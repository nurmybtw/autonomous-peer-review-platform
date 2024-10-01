import os
import time
import pandas as pd
import torch
from ast import literal_eval
from torch.utils.data import Dataset
from transformers import BertTokenizer, AutoTokenizer, AutoModelForSequenceClassification, Trainer as TrfTrainer, TrainingArguments, DataCollatorWithPadding
from adapters import AdapterTrainer, AutoAdapterModel

from ..train_utils.labels_encoder import LabelsEncoder
from ..gru_model.model import GRUModel
from ..train_utils.trainer import Trainer
from ..train_utils.compute_metrics import compute_metrics


class CustomDataset(Dataset):
    def __init__(self, dataframe, tokenizer, labels_encoder):
        self.tokenizer = tokenizer
        self.labels_encoder = labels_encoder
        self.abstracts = dataframe['abstract'].values.tolist()
        self.abstracts = self.tokenizer(self.abstracts, 
                                        max_length=256, 
                                        padding='max_length', 
                                        truncation=True, 
                                        return_tensors='pt')['input_ids']
        self.labels = [self.labels_encoder(category) for category in dataframe["categories"].values]

    def __len__(self):
        return len(self.abstracts)

    def __getitem__(self, idx):
        input_data = self.abstracts[idx]
        target_data = self.labels[idx]
        return input_data, target_data

def encode_labels(examples):
    examples['labels'] = labels_encoder(examples['labels'], return_tensors=False)
    return examples

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

############################ Choose evaluation model

eval_model = 'gru_model'
# eval_model = 'scibert'
# eval_model = 'scincl'
# eval_model = 'specter2'

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

############################ Dataset Prep

test_set = pd.read_csv('../data/arxiv_balanced_twothreelabel_test.csv')
test_set["categories"] = test_set["categories"].apply(lambda x: literal_eval(x))
test_set.drop(columns=['authors', 'primary_category'])

if eval_model == 'gru_model':
    test_ds = CustomDataset(
        test_set, 
        tokenizer, 
        labels_encoder
    )
else:
    test_dataset = Dataset.from_pandas(test_set)
    test_dataset = test_dataset.map(encode_labels)
    test_ds = test_dataset.map(tokenize_function, batched=True)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

############################ Model init

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

############################ Testing

st = time.time()
print('Test performance: ', end='')

if eval_model == 'gru_model':
    trainer = Trainer(
        model, 
        test_ds, 
        test_ds, 
        compute_metrics, 
        lr=1e-3, 
        task_config='multi-label-classification'
    )
    trainer.test()
elif eval_model == 'scibert' or eval_model == 'scincl':
    trainer = TrfTrainer(
        model=model,
        eval_dataset=test_ds,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    print(trainer.evaluate())
else:
    trainer = AdapterTrainer(
        model=model,
        eval_dataset=test_ds,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    print(trainer.evaluate())

et = time.time()
diff = et - st
time_per_1k = diff * 1000 / len(test_set)
print(f'Time per 1000 samples: {time_per_1k}')

model_params = sum(p.numel() for p in model.parameters())
print(f'Model parameters: {model_params}')

mem_params = sum(p.numel() * p.element_size() for p in model.parameters())
mem_buffers = sum(b.numel() * b.element_size() for b in model.buffers())
total_memory = mem_params + mem_buffers
print(f'Model size in memory: {total_memory / 1024**2}MB')