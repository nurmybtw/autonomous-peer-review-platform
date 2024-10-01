import os
import pandas as pd
from ast import literal_eval
from torch.utils.data import Dataset
from transformers import BertTokenizer

from ..train_utils.labels_encoder import LabelsEncoder
from .model import GRUModel
from ..train_utils.trainer import Trainer
from ..train_utils.compute_metrics import compute_metrics


class CustomDataset(Dataset):
    def __init__(self, dataframe, tokenizer, labels_encoder, task_config='multi-label-classification'):
        self.tokenizer = tokenizer
        self.abstracts = dataframe['abstract'].values.tolist()
        self.abstracts = self.tokenizer(self.abstracts, 
                                        max_length=256, 
                                        padding='max_length', 
                                        truncation=True, 
                                        return_tensors='pt')['input_ids']
        self.labels = dataframe["categories"].values
        self.labels_encoder = labels_encoder
        self.task_config = task_config

    def __len__(self):
        return len(self.abstracts)

    def __getitem__(self, idx):
        input_data = self.abstracts[idx]
        if self.task_config == 'multi-label-classification':
            target_data = self.labels_encoder(self.labels[idx])
        elif self.task_config == 'multi-class-classification':
            target_data = self.labels_encoder(self.labels[idx])[0]
        return input_data, target_data

################## Tokenizer Loading ####################

tokenizer = BertTokenizer.from_pretrained(
    './data/custom-wp-vocab-50k-vocab.txt', 
    local_files_only=True
)

################## Labels Encoder Loading ####################

labels_encoder = LabelsEncoder(task_config='multi-label-classification')
labels_encoder.load_labels('./data/labels.json')

################## Dataset Loading ####################

train_set = pd.read_csv('./data/arxiv_balanced_twothreelabel_train.csv')
train_set["categories"] = train_set["categories"].apply(lambda x: literal_eval(x))
train_set.drop(columns=['authors', 'primary_category'])
train_dataset = CustomDataset(
    train_set, 
    tokenizer, 
    labels_encoder, 
    task_config='multi-label-classification'
)

test_set = pd.read_csv('./data/arxiv_balanced_twothreelabel_test.csv')
test_set["categories"] = test_set["categories"].apply(lambda x: literal_eval(x))
test_set.drop(columns=['authors', 'primary_category'])
test_dataset = CustomDataset(
    test_set, 
    tokenizer, 
    labels_encoder, 
    task_config='multi-label-classification'
)

################## Model Init ####################

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

################## Training Init ####################

trainer = Trainer(
    model, 
    train_dataset, 
    test_dataset, 
    compute_metrics, 
    lr=1e-3, 
    task_config='multi-label-classification'
)

os.mkdir('./checkpoints')
trainer.train(
    num_epochs=10, 
    batch_size=256, 
    checkpoint_path='./checkpoints',
    save_checkpoint_rate=1,
    # resume_from_checkpoint='./checkpoints/checkpoint_epoch_10.pth'
)

trainer.test()