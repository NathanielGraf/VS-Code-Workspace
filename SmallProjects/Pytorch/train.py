import torch
import torch.optim as optim
import matplotlib.pyplot as plt

from env import CardGameEnv
from model import PolicyNetwork
from selfplay import run_self_play_episode, evaluate_win_rate
import numpy as np

# Configs
EPISODES = 50
EVAL_INTERVAL = 5
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Ellis was here she's the best <3
# Init env/model
dummy_env = CardGameEnv()
obs_size = len(dummy_env.get_observation_space())
act_size = (dummy_env.get_action_space())
policy_net = PolicyNetwork(input_dim=obs_size, action_dim=act_size).to(DEVICE)
optimizer = optim.Adam(policy_net.parameters(), lr=1e-3)

win_rates = []

loss_history = []

def moving_average(data, window_size=10):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Training loop
for episode in range(1, EPISODES + 1):
    data, _ = run_self_play_episode(CardGameEnv, policy_net, mcts_simulations=25)

    for state, pi, z in data:
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(DEVICE)
        pi_tensor = torch.FloatTensor(pi).unsqueeze(0).to(DEVICE)
        z_tensor = torch.FloatTensor([z]).to(DEVICE)

        pred_pi, pred_v = policy_net(state_tensor)
        loss_pi = -torch.sum(pi_tensor * torch.log(pred_pi + 1e-8))
        loss_v = (pred_v.squeeze() - z_tensor).pow(2).mean()
        loss = loss_pi + loss_v

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        loss_history.append(loss.item())
        


    # Periodic evaluation
    if episode % EVAL_INTERVAL == 0:
        win_rate = evaluate_win_rate(CardGameEnv, policy_net, num_games=20)
        win_rates.append(win_rate)

# Plotting
plt.plot(range(EVAL_INTERVAL, EPISODES + 1, EVAL_INTERVAL), win_rates)
plt.xlabel("Episodes")
plt.ylabel("Win Rate")
plt.title("Evaluation Win Rate Over Time")
plt.grid()
plt.savefig("win_rate_plot.png")
plt.show()



smoothed = moving_average(loss_history, window_size=10)

plt.plot(smoothed)
plt.xlabel("Episode")
plt.ylabel("Smoothed Loss")
plt.title("Smoothed Training Loss")
plt.grid(True)
plt.show()