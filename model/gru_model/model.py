import torch
import torch.nn as nn

class GRUModel(nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim, output_dim, n_layers=1, bidirectional=False, dropout=0.5):
        super().__init__()
        self.embedding = nn.Embedding(
            input_dim, 
            embedding_dim
        )
        self.gru = nn.GRU(
            embedding_dim, 
            hidden_dim, 
            num_layers=n_layers, 
            dropout=dropout, 
            batch_first=True, 
            bidirectional=bidirectional
        )
        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, text):
        # Word-embedding layer
        embedded = self.dropout(self.embedding(text))

        # Run through the GRU layers
        outputs, hidden = self.gru(embedded)

        # Bidirectional concat of the hidden states of the last layer (second layer)
        hidden = self.dropout(torch.cat((hidden[-2, :, :], hidden[-1, :, :]), dim=1))
        
        output = self.fc(hidden)
        return output, hidden