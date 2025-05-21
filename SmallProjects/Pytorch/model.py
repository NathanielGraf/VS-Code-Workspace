import torch
import torch.nn as nn
import torch.nn.functional as F


class PolicyNetwork(nn.Module):
    def __init__(self, input_dim=157, hidden_dim=128, action_dim=52):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim * 2)
        self.fc3 = nn.Linear(hidden_dim * 2, hidden_dim)
        self.policy_head = nn.Linear(hidden_dim, action_dim)
        self.value_head = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))

        raw_logits = self.policy_head(x)
        stabilized_logits = raw_logits - raw_logits.max(dim=1, keepdim=True).values
        action_probs = F.softmax(stabilized_logits, dim=-1)

        value = self.value_head(x)
        return action_probs, value

    def sample_subset(self, action_probs, mask, strategy="threshold"):
        """
        Samples a subset of actions (cards) from a policy vector.
        Supports threshold or top-k selection.
        """
        masked_probs = action_probs * mask
        total = masked_probs.sum(dim=1, keepdim=True)
        if total.item() == 0:
            # fallback to uniform random selection of cards still in deck
            indices = mask.squeeze(0).nonzero(as_tuple=True)[0]
            selected_indices = torch.randint(0, len(indices), (1,)).item()
            return [indices[selected_indices].item()]
        
        else:
            normalized_probs = masked_probs / total

            if strategy == "threshold":
                card_counts = mask.sum(dim=1, keepdim=True)
                threshold = 1.0 / (card_counts + 1e-8)
                chosen = (normalized_probs > threshold).float()
            elif strategy == "topk":
                k = max(1, int(mask.sum().item() * 0.3))
                topk = torch.topk(normalized_probs, k=k, dim=1).indices
                chosen = torch.zeros_like(normalized_probs)
                chosen.scatter_(1, topk, 1.0)
            else:
                raise ValueError("Unknown subset selection strategy")

            selected_indices = [i for i, p in enumerate(chosen[0]) if p > 0]
            return selected_indices

