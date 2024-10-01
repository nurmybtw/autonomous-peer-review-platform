import os
import json
import numpy as np
import torch
import torch.nn as nn
from transformers import BertTokenizer
from .labels_encoder import LabelsEncoder


class GRUModel(nn.Module):
    def __init__(self, 
                 input_dim, 
                 embedding_dim, 
                 hidden_dim, 
                 output_dim, 
                 n_layers, 
                 bidirectional, 
                 dropout=0.5):
        super().__init__()
        self.embedding = nn.Embedding(input_dim, embedding_dim)
        self.gru = nn.GRU(embedding_dim, hidden_dim, num_layers=n_layers, dropout=dropout, batch_first=True, bidirectional=bidirectional)
        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, text):
        embedded = self.dropout(self.embedding(text))
        _, hidden = self.gru(embedded)
        hidden = self.dropout(torch.cat((hidden[-2, :, :], hidden[-1, :, :]), dim=1))
        output = self.fc(hidden)
        return output, hidden
    
class PaperReviewerModel:
    def __init__(self):
        self.model_config = self.load_model_config()
        self.tokenizer = self.load_tokenizer()
        self.labels_encoder = LabelsEncoder()
        self.labels_encoder.load_labels()
        self.model = GRUModel(self.model_config['vocab_size'], 
                              self.model_config['embedding_dim'], 
                              self.model_config['hidden_dim'], 
                              self.model_config['num_classes'], 
                              self.model_config['num_layers'], 
                              self.model_config['bidirectional'])
        self.load_model_params()

    def load_tokenizer(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        vocab_path = 'params/vocab.txt'
        return BertTokenizer.from_pretrained(os.path.join(current_dir, vocab_path), local_files_only=True)

    def load_model_config(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = 'params/config.json'
        with open(os.path.join(current_dir, config_path), 'r') as config_file:
            model_config = json.load(config_file)
        return model_config

    def load_model_params(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        params_path = 'params/model_checkpoint.pth'
        checkpoint = torch.load(os.path.join(current_dir, params_path), map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

    def get_categories(self, abstracts, k=3):
        with torch.no_grad():
            outputs, _ = self.model(self.tokenizer(abstracts, 
                                                   max_length=256, 
                                                   padding='max_length', 
                                                   truncation=True, 
                                                   return_tensors='pt')['input_ids'])
        for output in outputs.cpu().numpy():
            categories = []
            top_k = np.argsort(output)[-k:]
            mask = np.zeros_like(output)
            mask[top_k] = 1
            categories.append(self.labels_encoder.decode(mask.reshape(1, -1))[0])
        return categories

    def get_embeddings(self, abstracts):
        with torch.no_grad():
            _, hidden = self.model(self.tokenizer(abstracts, 
                                                   max_length=256, 
                                                   padding='max_length', 
                                                   truncation=True, 
                                                   return_tensors='pt')['input_ids'])
        return hidden.cpu().numpy()

pare = PaperReviewerModel()
print('Loaded Model Successfully')