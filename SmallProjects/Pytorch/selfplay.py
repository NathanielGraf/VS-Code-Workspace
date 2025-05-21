import random
import torch
import numpy as np
from collections import deque
from tqdm import tqdm

from env import CardGameEnv
from model import PolicyNetwork
from mcts import MCTS

class SelfPlayTrainer:
    def __init__(self, env, policy_network, mcts_simulations=50, replay_buffer_size=10000, batch_size=32):
        self.env = env
        self.policy_network = policy_network
        self.mcts_simulations = mcts_simulations
        self.replay_buffer = deque(maxlen=replay_buffer_size)
        self.batch_size = batch_size
        self.optimizer = torch.optim.Adam(policy_network.parameters(), lr=1e-3)

    def run_self_play_episode(self):
        state = self.env.reset()
        episode_data = []
        done = False

        while not done:
            
            # Run MCTS to get improved policy
           
            mcts = MCTS(CardGameEnv, policy_network)

            # Make sure to clone env state before passing it to MCTS
            env_state = env.clone_state()
            policy = mcts.run_simulations(env_state, num_simulations=50)

            # Convert to torch tensor for training format
            action_probs = torch.FloatTensor(policy).unsqueeze(0)


            mask = torch.FloatTensor(state[-52:]).unsqueeze(0)
            masked_probs = action_probs * mask
            normalized_probs = masked_probs / masked_probs.sum()

            # Sample a subset of cards above a threshold (alpha-zero style distribution)   
            selected_indices = self.policy_network.sample_subset(normalized_probs, mask, strategy="threshold")

            probs = normalized_probs.squeeze(0)
            episode_data.append((state, probs.detach().numpy(), None))  # z will be filled later

            state, reward, done, _, win = self.env.step(selected_indices)

        # Assign z to each state in episode
        z = 1 if win == 1 else -1
        episode_data = [(s, p, z) for (s, p, _) in episode_data]
        self.replay_buffer.extend(episode_data)

    def train_policy_network(self, epochs=1):
        if len(self.replay_buffer) < self.batch_size:
            return

        for _ in range(epochs):
            batch = random.sample(self.replay_buffer, self.batch_size)
            states, policy_targets, zs = zip(*batch)

            states_tensor = torch.FloatTensor(states)
            policy_targets_tensor = torch.FloatTensor(np.array(policy_targets))
            zs_tensor = torch.FloatTensor(zs).unsqueeze(1)

            action_probs, state_values = self.policy_network(states_tensor)
            log_probs = torch.log(action_probs + 1e-8)

            policy_loss = -torch.mean(torch.sum(policy_targets_tensor * log_probs, dim=1))
            value_loss = torch.mean((zs_tensor - state_values) ** 2)
            loss = policy_loss + value_loss

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
    # Episodes 1000 eval 100 default
    def train(self, total_episodes=50, eval_interval=5):
        win_rates = []
        for episode in tqdm(range(1, total_episodes + 1)):
            self.run_self_play_episode()
            self.train_policy_network()

            if episode % eval_interval == 0:
                win_rate = self.evaluate_win_rate()
                win_rates.append(win_rate)
                print(f"Episode {episode}: Win Rate = {win_rate:.2f}")
        return win_rates

    def evaluate_win_rate(self, games=5):
        wins = 0
        for _ in range(games):
            state = self.env.reset()
            done = False
            while not done:
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                with torch.no_grad():
                    action_probs, _ = self.policy_network(state_tensor)
                mask = torch.FloatTensor(state[-52:]).unsqueeze(0)
                masked_probs = action_probs * mask
                normalized_probs = masked_probs / masked_probs.sum()
                    
                selected_indices = self.policy_network.sample_subset(normalized_probs, mask, strategy="threshold")
                    
                state, reward, done, _, win = self.env.step(selected_indices)
            if win == 1:
                wins += 1
        return wins / games



env = CardGameEnv()
observation_space = env.get_observation_space()
action_space = env.get_action_space()
policy_network = PolicyNetwork(input_dim=len(observation_space), action_dim=action_space)
trainer = SelfPlayTrainer(env, policy_network)
win_rates = trainer.train(total_episodes=50, eval_interval=5)

import matplotlib.pyplot as plt

# win_rates is a list with one entry per 100 episodes
episodes_axis = [100 * (i+1) for i in range(len(win_rates))]

plt.plot(episodes_axis, win_rates, marker='o')
plt.xlabel("Episodes")
plt.ylabel("Win Rate")
plt.title("Training Win Rate Over Time")
plt.grid(True)
plt.show()
