import torch
import torch.nn as nn
import torch.nn.functional as F


class PolicyNetwork(nn.Module):
    def __init__(self, obs_dim, n_cards, hidden_dim=256):
        super().__init__()
        self.fc1 = nn.Linear(obs_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, hidden_dim)
        self.policy_head = nn.Linear(hidden_dim, n_cards)
        self.value_head = nn.Linear(hidden_dim, 1)

    def forward(self, x, mask=None):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        
        logits = self.policy_head(x) 
        if mask is not None:
            # mask: 1 for available cards, 0 otherwise
            logits = logits.masked_fill(mask == 0, -1e9)

        probs = torch.sigmoid(logits)
        value = torch.tanh(self.value_head(x)).squeeze(1)
        return logits, probs, value
    
