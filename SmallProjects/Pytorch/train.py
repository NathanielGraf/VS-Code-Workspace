import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.distributions import Categorical

from env import CardGameEnv
from model import PolicyNetwork
import numpy as np



#Ellis was here she's the best <3

# hyperparams/configs
num_episodes = 10000
gamma = .99           # since reward only comes at end, you can leave this at 1
lr = 1e-4
value_coef = 0.5       # weight for value loss
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# init
env = CardGameEnv()
obs_size = len(env.get_observation_space())
act_size = env.get_action_space()
policy_net = PolicyNetwork(input_dim=obs_size, action_dim=act_size).to(device)
optimizer = optim.Adam(policy_net.parameters(), lr=lr)

policy_losses   = []
value_losses    = []
total_losses    = []
win_history     = []   # 1 if win, 0 if lose
avg_win_rate    = []
avg_loss        = []
log_interval    = 50   # how often you compute/plot a running average

for episode in range(1, num_episodes + 1):
    state = env.reset()
    #ep_loss = 0
    #ep_reward = 0
    
    log_probs = []
    values    = []
    rewards   = []

    done = False
    while not done:
        # forward pass
        state_t = torch.FloatTensor(state).unsqueeze(0).to(device)
        mask_t = torch.FloatTensor(env.get_action_mask()).unsqueeze(0).to(device)
        
        logits, probs, value = policy_net(state_t, mask_t)
        dist = torch.distributions.Bernoulli(probs)

        action_sample = dist.sample()
        
        if action_sample.sum() == 0:
            available = mask_t.nonzero(as_tuple=False)
            idx = available[torch.randint(len(available), (1,))]
            action_sample[0, idx] = 1

        logp = dist.log_prob(action_sample).sum(dim=1)  # total log-prob

        # turn binary mask into list of indices
        selected_indices = action_sample.squeeze(0).nonzero(as_tuple=True)[0].tolist()

        next_state, reward, done, _, _ = env.step(selected_indices)

        # record
        log_probs.append(logp)
        values.append(value.squeeze(0))
        rewards.append(reward)

        state = next_state

    # compute returns (R_t = sum_{k=t..T} γ^{k-t} r_k)
    returns = []
    R = 0
    for r in reversed(rewards):
        R = r + gamma * R
        returns.insert(0, R)
    returns = torch.tensor(returns).to(device)
    values = torch.stack(values)
    log_probs = torch.stack(log_probs)

    # advantage = R - V(s)
    advantage = returns - values
    # normalize advantage
    advantage = (advantage - advantage.mean()) / (advantage.std() + 1e-8)
    

    # losses
    policy_loss = -(log_probs * advantage.detach()).mean()
    value_loss  = advantage.pow(2).mean()
    
    ent = dist.entropy().sum(dim=1).mean()
    loss = policy_loss + value_coef * value_loss - 1e-2 * ent
    
    policy_losses.append(policy_loss.item())
    value_losses.append(value_loss.item())
    total_losses.append((policy_loss+value_coef*value_loss).item())
    win_history.append(int(returns[0]>0))

    # backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if episode % 50 == 0:
        print(f"Episode {episode}\tLoss: {loss.item():.3f}\tReturn: {returns[0]:.3f}")


# moving average for win‐rate
def moving_average(x, w=100):
    return np.convolve(x, np.ones(w)/w, mode='valid')

# smooth both curves over 100 episodes
smoothed_policy = moving_average(policy_losses, w=100)
smoothed_value  = moving_average(value_losses, w=100)
smoothed_loss = moving_average(total_losses, w=100)
smoothed_win  = moving_average(win_history, w=100)

fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# top-left: total loss
axs[0, 0].plot(smoothed_loss)
axs[0, 0].set_title("Smoothed Total Loss (w=100)")
axs[0, 0].set_xlabel("Episode")
axs[0, 0].set_ylabel("Loss")

# top-right: policy loss
axs[0, 1].plot(smoothed_policy)
axs[0, 1].set_title("Smoothed Policy Loss (w=100)")
axs[0, 1].set_xlabel("Episode")
axs[0, 1].set_ylabel("Policy Loss")

# bottom-left: value loss
axs[1, 0].plot(smoothed_value)
axs[1, 0].set_title("Smoothed Value Loss (w=100)")
axs[1, 0].set_xlabel("Episode")
axs[1, 0].set_ylabel("Value Loss")

# bottom-right: win rate
axs[1, 1].plot(smoothed_win)
axs[1, 1].set_title("Smoothed Win Rate (w=100)")
axs[1, 1].set_xlabel("Episode")
axs[1, 1].set_ylabel("Win Rate")

plt.tight_layout()
plt.show()
