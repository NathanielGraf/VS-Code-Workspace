import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.distributions import Bernoulli
import random
import copy
from concurrent.futures import ProcessPoolExecutor
import os
from multiprocessing import Pool

from env import CardGameEnv
from model import PolicyNetwork
import numpy as np



#Ellis was here she's the best <3

def rollout_worker(args):
    """
    Perform exactly one policy‐driven simulation from a given snapshot.
    args is a tuple: (state_snapshot, net_state_dict, device)
    Returns 1 if win, else 0.
    """
    state_snapshot, net_weights, device = args

    # 1) Rebuild env
    sim = CardGameEnv()
    sim.load_state(state_snapshot)

    # 2) Rebuild policy net
    obs_dim = len(sim.get_observation_space())
    act_dim = sim.get_action_space()
    net     = PolicyNetwork(obs_dim, act_dim).to(device)
    net.load_state_dict(net_weights)
    net.eval()

    # 3) Play to terminal
    done = False
    last_win = 0
    while not done:
        s_t   = torch.FloatTensor(sim.get_observation_space())\
                       .unsqueeze(0).to(device)
        m_t   = torch.FloatTensor(sim.get_action_mask())\
                       .unsqueeze(0).to(device)
        _, probs, _ = net(s_t, m_t)
        dist = Bernoulli(probs)
        a_mask = dist.sample().squeeze(0).cpu().numpy()

        # enforce non-empty
        if a_mask.sum() == 0:
            avail = np.nonzero(m_t.cpu().numpy())[1]
            a_mask[random.choice(avail)] = 1

        action = a_mask.nonzero()[0].tolist()
        _, _, done, _, win_flag = sim.step(action)
        last_win = win_flag

    return last_win

def rollout_worker_random(args):
    """
    Perform exactly one random sim from a given snapshot.
    args is a tuple: (state_snapshot, net_state_dict, device)
    Returns 1 if win, else 0.
    """
    state_snapshot, net_weights, device = args

    # 1) Rebuild env
    sim = CardGameEnv()
    sim.load_state(state_snapshot)

    # 2) Play to terminal
    done = False
    last_win = 0
    
    while not done:
        # pick a random subset
        mask = sim.get_action_mask()                 
        avail = [i for i,m in enumerate(mask) if m]     # indices of valid cards

        # build a random subset: for each avail card flip a fair coin
        subset = [i for i in avail if random.random() < 0.5]

        # if we got the empty set, force at least one pick
        if not subset:
            subset = [random.choice(avail)]

        # step with that subset
        _, _, done, _, win_flag = sim.step(subset)
        last_win = win_flag

    return last_win

def random_potential(env, net, _pool, num_sims=50, device="cuda"):
    """
    Estimate P(win | s) by simulating the rest of the game
    using *random actions*, but batching all net calls.
    """
    
    # 1) Take one snapshot of the real env
    initial_state = env.get_state()
    net_weights = net.state_dict()

    args = [(initial_state, net_weights, device) for _ in range(num_sims)]

    wins = 0 
    
    wins = _pool.map(rollout_worker_random, args)

    return sum(wins) / num_sims

def policy_potential(env, net, _pool, num_sims=50, device="cuda"):
    """
    Estimate P(win | s) by simulating the rest of the game
    using *your current policy*, but batching all net calls.
    """
    num_sims = 200
    
    # 1) Take one snapshot of the real env
    initial_state = env.get_state()
    net_weights = net.state_dict()

    args = [(initial_state, net_weights, device) for _ in range(num_sims)]

    wins = 0 
    
    wins = _pool.map(rollout_worker, args)

    return sum(wins) / num_sims

def main():
    """
    Main function to train the policy network.
    """
    
    # hyperparams/configs
    num_episodes = 10000
    gamma = .99      
    lr = 1e-5
    lam = 0.95       # GAE λ
    ent_coef = 0.05   # weight for entropy loss
    value_coef = 1      # weight for value loss
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # init
    env = CardGameEnv()
    obs_size = len(env.get_observation_space())
    act_size = env.get_action_space()
    policy_net = PolicyNetwork(obs_dim=obs_size, n_cards=act_size).to(device)
    optimizer = optim.Adam(policy_net.parameters(), lr=lr)

    policy_losses   = []
    value_losses    = []
    total_losses    = []
    deltas   = []
    phis     = []
    win_history     = []   # 1 if win, 0 if lose

    WORKERS = min(4, os.cpu_count() or 1)
    _pool   = Pool(processes=WORKERS)


    for episode in range(1, num_episodes + 1):
        state = env.reset()
        #print("Episode: ", episode)
        done = False
        
        # per-episode storage
        logps, values, rewards, dones, entropies = [], [], [], [], []
    
        #potential 
        #phi_t = policy_potential(env, policy_net, _pool, num_sims=50, device=device)
        
        # 1) Compute initial V(s_0)
        s0 = torch.FloatTensor(state).unsqueeze(0).to(device)
        m0 = torch.FloatTensor(env.get_action_mask()).unsqueeze(0).to(device)
        _, _, v0 = policy_net(s0, m0)
        v_t = v0.detach()   # detach so GAE won't backprop through it
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
            ent = dist.entropy().sum(dim=1)  # entropy

            chosen_action = action_sample.squeeze(0).nonzero(as_tuple=True)[0].tolist()
            
            next_state, reward, done, _, win = env.step(chosen_action)
            
            with torch.no_grad():
                if not done:
                    next_state_t = torch.FloatTensor(next_state).unsqueeze(0).to(device)
                    mask_t = torch.FloatTensor(env.get_action_mask()).unsqueeze(0).to(device)
                    _, _, next_value = policy_net(next_state_t, mask_t)
                else:
                    #next_value = torch.zeros_like(value).to(device)
                    next_value = torch.zeros_like(value)
            
            # inside your episode loop, before sampling the real action:
            #phi_tp1 = policy_potential(env, policy_net, _pool, num_sims=50, device=device)
            v_tp1  = next_value.detach()   # detach so GAE won't backprop through it
            shaped   = (gamma * v_tp1 - v_t).item()
            total_r  = reward + shaped
            
            
            logps.append(logp)
            values.append(v_t)
            rewards.append(total_r)
            dones.append(done)
            entropies.append(ent)
            
            # clip gradients
            #torch.nn.utils.clip_grad_norm_(policy_net.parameters(), max_norm=0.5)
            
            state = next_state
            v_t = v_tp1

        # append final bootstrap value = 0 at terminal
        values.append(torch.zeros_like(v_t).to(device))
        
        # —— GAE/Lambda computation —— 
        advantages = []
        gae = 0.0
        # reverse through time
        for t in reversed(range(len(rewards))):
            delta = rewards[t] + gamma * values[t+1] * (1 - dones[t]) - values[t]
            gae   = delta + gamma * lam * (1 - dones[t]) * gae
            advantages.insert(0, gae)
        advantages = torch.stack(advantages).to(device)
        returns    = advantages + torch.stack(values[:-1])
        
            # —— Losses & update —— 
        logps_tensor   = torch.stack(logps)
        values_tensor  = torch.stack(values[:-1])
        ent_tensor     = torch.stack(entropies)

        policy_loss = - (logps_tensor * advantages.detach()).mean()
        value_loss  = (returns - values_tensor).pow(2).mean()
        entropy_loss= - ent_tensor.mean()

        loss = policy_loss + value_coef * value_loss + ent_coef * entropy_loss

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy_net.parameters(), max_norm=0.5)
        optimizer.step()

        # logging
        policy_losses.append(policy_loss.item())
        value_losses.append(value_loss.item())
        total_losses.append(loss.item())
        win_history.append(int(win))
            
        if episode % 50 == 0:
            avg_reward = np.mean(rewards)
            avg_value = torch.mean(torch.stack(values)).item()
            avg_policy_loss = np.mean(policy_losses[-50:])
            avg_value_loss = np.mean(value_losses[-50:])
            avg_total_loss = np.mean(total_losses[-50:])
            
            print(f"Episode {episode}/{num_episodes} | "
                f"Avg Reward: {avg_reward:.2f} | "
                f"Avg Value: {avg_value:.2f} | "
                f"Avg Policy Loss: {avg_policy_loss:.2f} | "
                f"Avg Value Loss: {avg_value_loss:.2f} | "
                f"Avg Total Loss: {avg_total_loss:.2f} | "
                f"Win Rate: {np.mean(win_history[-50:]):.2f}")
            
        #print("Advantage stats:", advantages.mean().item(), advantages.std().item())
    
    
    # smooth both curves over episodes
    episodes = 100
    smoothed_policy = moving_average(policy_losses, w=episodes)
    smoothed_value  = moving_average(value_losses, w=episodes)
    smoothed_loss = moving_average(total_losses, w=episodes)
    smoothed_win  = moving_average(win_history, w=episodes)

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
    
    # start a brand-new figure for your diagnostics
    plt.figure(figsize=(12,4))

    # left: TD-error histogram
    plt.subplot(1,2,1)
    plt.hist(deltas, bins=50)
    plt.title("TD-Error δ")
    plt.xlabel("δ")
    plt.ylabel("Count")

    # right: φ before / after
    plt.subplot(1,2,2)
    xs = np.array(phis)
    plt.plot(xs[:,0], label="φ_t")
    plt.plot(xs[:,1], label="φ_tp1")
    plt.title("Potential before/after")
    plt.xlabel("Step")
    plt.legend()

    plt.tight_layout()
    plt.show()
    
    _pool.close()
    _pool.join()




# moving average for win‐rate
def moving_average(x, w=100):
    return np.convolve(x, np.ones(w)/w, mode='valid')

if __name__ == "__main__":
    main()
    
