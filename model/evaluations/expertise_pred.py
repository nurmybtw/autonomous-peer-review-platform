import os
from transformers import AutoTokenizer, BertTokenizer
from sentence_transformers.util import cos_sim
import torch
import os
from transformers import BertTokenizer, AutoTokenizer, AutoModelForSequenceClassification
from adapters import AutoAdapterModel
from ..gru_model.model import GRUModel
from ..train_utils.labels_encoder import LabelsEncoder
from .gold_ds_predictor import GoldDatasetPredictor

eval_model = 'gru_model'

############################ Tokenizer

if eval_model == 'gru_model':
    tokenizer = BertTokenizer.from_pretrained(
        '../data/custom-wp-vocab-50k-vocab.txt', 
        local_files_only=True
    )
elif eval_model == 'scibert':
    tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
elif eval_model == 'scincl':
    tokenizer = AutoTokenizer.from_pretrained('malteos/scincl')
else:
    tokenizer = AutoTokenizer.from_pretrained('allenai/specter2_base')

############################ Labels Encoder

labels_encoder = LabelsEncoder(task_config='multi-label-classification')
labels_encoder.load_labels('../data/labels.json')

############################ Model Init

if eval_model == 'gru_model':
    INPUT_DIM = len(tokenizer)
    EMBEDDING_DIM = 256
    HIDDEN_DIM = 256
    OUTPUT_DIM = len(labels_encoder)
    N_LAYERS = 2
    BIDIRECTIONAL = True
    DROPOUT = 0.5

    model = GRUModel(
        INPUT_DIM, 
        EMBEDDING_DIM, 
        HIDDEN_DIM, 
        OUTPUT_DIM, 
        N_LAYERS, 
        BIDIRECTIONAL, 
        DROPOUT
    )
    checkpoint = torch.load('../model_params/gru_model/model_checkpoint.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
elif eval_model == 'scibert':
    model = AutoModelForSequenceClassification.from_pretrained(
        'allenai/scibert_scivocab_uncased', 
        num_labels=len(labels_encoder)
    )
    model.config.problem_type = 'multi_label_classification'
elif eval_model == 'scincl':
    model = AutoModelForSequenceClassification.from_pretrained(
        'malteos/scincl', 
        num_labels=len(labels_encoder)
    )
    model.config.problem_type = 'multi_label_classification'
else:
    model = AutoAdapterModel.from_pretrained('allenai/specter2_base')
    model.add_classification_head("mlbcls", num_labels=len(labels_encoder), multilabel=True)
    model.add_adapter("mlbcls")
    model.train_adapter("mlbcls")
    model.set_active_adapters("mlbcls")

model.eval()
model.to('cuda:0')

############################ Testing

if eval_model == 'gru_model':
    def get_embedding(abstract):
        abstracts = [abstract]
        tokenized_abstracts = tokenizer(abstracts, max_length=256, 
                                            padding='max_length', 
                                            truncation=True, 
                                            return_tensors='pt')['input_ids']
        tokenized_abstracts = tokenized_abstracts.to('cuda:0')
        with torch.no_grad():
            _, hidden = model(tokenized_abstracts)
        return hidden.cpu().numpy()[0]
else:
    def get_embedding(abstract):
        abstracts = [abstract]
        inputs = tokenizer(abstracts, max_length=512, 
                                            padding='max_length', 
                                            truncation=True, 
                                            return_tensors='pt')
        inputs = inputs.to('cuda:0')
        with torch.no_grad():
            outputs = model(**inputs)
        hidden = outputs.last_hidden_state
        return hidden[0, 0, :].cpu().numpy()


dataset_dir = '../data/gold-pare-dataset-d-20'
os.mkdir('gold_ds_preds')
preds_dir = './gold_ds_preds'
gold_eval = GoldDatasetPredictor(get_embedding, 768, cos_sim, dataset_dir, preds_dir, eval_model)
gold_eval.precompute_embeddings()
gold_eval.predict()