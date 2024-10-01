import json
import os
import torch
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

class LabelsEncoder:
    def __init__(self):
        self.mlb = MultiLabelBinarizer()
        
    def load_labels(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        labels_path = 'params/labels.json'
        with open(os.path.join(current_dir, labels_path), 'r') as labels_file:
            classes = json.load(labels_file)
        self.mlb.fit([list(classes.keys())])
            
    def __len__(self):
        return len(self.mlb.classes_)
    
    def decode(self, labels):
        return self.mlb.inverse_transform(labels)