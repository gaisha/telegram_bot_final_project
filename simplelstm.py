import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

class SimpleLSTM(nn.Module):
    def __init__(self, n_vocab, hidden_dim, embedding_dim, dropout=0.2, **kwargs):
        super(SimpleLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.embedding_dim = embedding_dim
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, dropout=dropout, num_layers=2)
        self.embeddings = nn.Embedding(n_vocab, embedding_dim)
        self.fc = nn.Linear(hidden_dim, n_vocab)
        self.kwargs = kwargs

    def forward(self, seq_in):
        embedded = self.embeddings(seq_in.t())
        lstm_out, _ = self.lstm(embedded)
        ht=lstm_out[-1]
        out = self.fc(ht)
        return out