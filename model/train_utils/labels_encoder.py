import json
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
import torch

class LabelsEncoder:
    def __init__(self, task_config='multi-label-classification'):
        self.task_config = task_config
        self.mlb = MultiLabelBinarizer()
        self.le = LabelEncoder()
        
    def load_labels(self, labels_path):
        with open(labels_path, 'r') as f:
            self.label_set = json.load(f)
        self.mlb.fit([list(self.label_set.keys())])
        self.le.fit(list(self.label_set.keys()))
        
    def save_labels(self, save_path=''):
        with open(f'{save_path}/labels.json', 'w') as f:
            json.dump(self.label_set, f)
            
    def __len__(self):
        return len(self.le.classes_)
    
    def __call__(self, label, return_tensors='pt'):
        if self.task_config == 'multi-label-classification':
            res = self.mlb.transform([label])[0].astype(np.float32)
        elif self.task_config == 'multi-class-classification':
            res = self.le.transform(label)
        if return_tensors == 'pt':
            res = torch.tensor(res)
        return res