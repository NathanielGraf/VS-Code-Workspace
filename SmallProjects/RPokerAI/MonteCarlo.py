import random
import math
import custom_env
import numpy as np
import random

class GameState:
    def __init__(self, env):
        self.env = env
        self.current_state = None
        self.done = False

    def take_action(self, action):
        if not self.done:
            next_state = self.env.step(action)
            self.current_state = next_state['next_state']
            self.done = next_state['done']
            return self.current_state, next_state['reward']
        else:
            return self.current_state, 0

# Usage
env = custom_env.CustomCardGameEnv()  # Replace with your environment initialization
game_state = GameState(env)


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.value = 0

def select(node, exploration_weight=1.0):
    """Select a child node using UCB1 formula."""
    if not node.children:
        return node

    # UCB1 calculation for child nodes
    best_child = None
    best_score = -float('inf')

    for child in node.children:
        if child.visits == 0:
            return child

        exploitation = child.value / child.visits
        exploration = math.sqrt(2 * math.log(node.visits) / child.visits)
        score = exploitation + exploration

        if score > best_score:
            best_score = score
            best_child = child

    return best_child

def expand(node, action):
    game_state = GameState(env)
    print("Action: ", action)
    child_state, reward = game_state.take_action(action)
    child_node = Node(state=child_state, parent=node, action=action, reward=reward)
    node.children.append(child_node)
    return child_node


def simulate(node):
    """Simulate a game from the given node and return the final reward."""
    state = node.state
    while not state['done']:
        # Random action selection for simulation
        action = [random.randint(0, 1) for _ in range(52)]
        state = env.step(action)['next_state']
    return state['reward']

def backpropagate(node, reward):
    """Backpropagate the reward up the tree."""
    while node is not None:
        node.visits += 1
        node.value += reward
        node = node.parent



def monte_carlo_search(env, num_iterations):
    """Monte Carlo Search algorithm."""
    root_state = env.reset()
    root_node = Node(state=root_state)

    for _ in range(num_iterations):
        node = root_node

        # Selection phase
        while not node.state[-1] == 1 and node.children:
            node = select(node)

        # Expansion phase
        if not node.state[-1] == 1:
            action = env.action_space.sample()
            while action in [child.action for child in node.children]:
                action = env.action_space.sample()
            
            node = expand(node, action)

        # Simulation phase
        reward = simulate(node)

        # Backpropagation phase
        backpropagate(node, reward)

    # Select the best action based on visit counts
    best_action = max(root_node.children, key=lambda x: x.visits).action
    return best_action






# Example usage
env = custom_env.CustomCardGameEnv()
best_action = monte_carlo_search(env, num_iterations=10000)
print("Best Action:", best_action)



