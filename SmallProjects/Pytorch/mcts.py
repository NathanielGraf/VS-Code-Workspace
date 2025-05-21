import torch
import math
from model import PolicyNetwork
from copy import deepcopy

class MCTSNode:
    def __init__(self, state, parent=None, prior=0.0):
        self.state = state
        self.parent = parent
        self.prior = prior
        self.visit_count = 0
        self.value_sum = 0.0
        self.children = {}  # action -> MCTSNode

    def value(self):
        if self.visit_count <= 0:
            return 0.0
        
        avg = self.value_sum / self.visit_count
        
         # catch any NaN or Inf
        if not math.isfinite(avg):
            return 0.0
        
        return avg

    def is_expanded(self):
        return len(self.children) > 0


class MCTS:
    def __init__(self, env_class, policy_net, device="cpu", c_puct=1.0):
        self.env_class = env_class
        self.policy_net = policy_net
        self.device = device
        self.c_puct = c_puct

    def run_simulations(self, root_state, num_simulations=50):
        self.root = MCTSNode(root_state)

        for _ in range(num_simulations):
            env = self.env_class()  # Create fresh environment per sim
            env.load_state(deepcopy(root_state))  # Needs to be implemented in env
            self._simulate(env, self.root)

        # Build final policy from visit counts
        total_visits = sum(child.visit_count for child in self.root.children.values())
        action_probs = [0.0] * 52
        for action, child in self.root.children.items():
            action_probs[action] = child.visit_count / total_visits

        return action_probs

    def _simulate(self, env, node):
        if env.is_terminal():
            reward = env.calculate_reward()
            return reward

        if not node.is_expanded():
            return self._expand_and_evaluate(env, node)

        # Selection: pick action with max UCT
        total_visits = sum(child.visit_count for child in node.children.values())
        best_score = -float("inf")
        best_action = None
        for action, child in node.children.items():
            uct = child.value() + self.c_puct * child.prior * math.sqrt(total_visits) / (1 + child.visit_count)
            if uct > best_score:
                best_score = uct
                best_action = action

        # Apply best action
        env.step([best_action])
        child_node = node.children[best_action]
        value = self._simulate(env, child_node)

        # Backpropagate
        child_node.value_sum += value
        child_node.visit_count += 1
        return value

    def _expand_and_evaluate(self, env, node):
        obs = torch.FloatTensor(env.get_observation_space()).unsqueeze(0).to(self.device)
        with torch.no_grad():
            action_probs, value = self.policy_net(obs)

        mask = torch.FloatTensor(env.get_action_mask()).unsqueeze(0).to(self.device)
        masked_probs = action_probs * mask
        normalized_probs = masked_probs / (masked_probs.sum() + 1e-8)

        for i in range(52):
            if mask[0, i] > 0:
                node.children[i] = MCTSNode(env.clone_state(), parent=node, prior=normalized_probs[0, i].item())

        node.value_sum += value.item()
        node.visit_count += 1
        return value.item()