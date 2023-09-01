import gym
import numpy as np
import itertools
from custom_env import CustomCardGameEnv



class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.99, epsilon=0.1):
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.action_space = np.array(self.generate_action_space())
        self.state_space = env.observation_space['player_hand'].shape[0]  # Modify this according to your observation space

        # Initialize the Q-table with zeros
        self.q_table = np.zeros((self.state_space, len(self.action_space)))
    
    @staticmethod
    def generate_action_space():
        # Define the maximum number of cards the agent can choose (up to 26)
        max_cards_to_choose = 1

        # Create all possible combinations of up to 26 cards from a 52-card deck
        action_space = []
        for num_cards_to_choose in range(1, max_cards_to_choose + 1):
            # Generate combinations of cards to choose
            combinations = itertools.combinations(range(52), num_cards_to_choose)
            
            # Append combinations to the action space
            action_space.extend(combinations)
        
        # Convert the combinations to lists
        action_space = [list(cards) for cards in action_space]

        return action_space

    def choose_action(self, state):
        # Epsilon-greedy policy
        if np.random.uniform(0, 1) < self.epsilon:
            return self.env.action_space.sample()  # Explore
        else:
            
            player_hand = np.array(state['player_hand'])
            print("Player Hand:", player_hand)
            #print("Player Hand:", player_hand)
            dealer_hand = np.array(state['dealer_hand'])
            print("Dealer Hand:", dealer_hand)
            #print("Dealer Hand:", dealer_hand)
        
            round_number = np.array(state['round_number'])
            print("Round Number:", round_number)
           
            
            state_array = np.concatenate((player_hand, dealer_hand, [round_number]))
            print("Len State Tuple:", len(state_array))
            print("State Tuple:", state_array)
            print("Q-table shape:", self.q_table.shape)
            return np.argmax(self.q_table[state_array, :])  # Exploit

    def update_q_table(self, state, action, reward, next_state):
        
        print("Next State:", next_state)
        
        best_next_action = np.argmax(self.q_table[next_state, :])
        current_value = self.q_table[state, action]
        learned_value = reward + self.discount_factor * self.q_table[next_state, best_next_action]
        self.q_table[state, action] = (1 - self.learning_rate) * current_value + self.learning_rate * learned_value

    def train(self, num_episodes):
        for episode in range(num_episodes):
            state = env.reset()
            total_reward = 0

            while True: 
                action = self.choose_action(state)
                selected_action = agent.action_space[action]
                #print("Action Space:", agent.action_space)
                #print("Action:", action)
                #print("Selected Action:", selected_action)
                next_state, reward, done, _ = env.step(selected_action)

                # Update Q-table
                self.update_q_table(state, action, reward, next_state)

                total_reward += reward
                state = next_state

                if done:
                    break

            print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

        print("Training finished.")

    def play(self, num_episodes):
        for episode in range(num_episodes):
            state = env.reset()
            total_reward = 0

            while True:
                action = np.argmax(self.q_table[state, :])
                next_state, reward, done, _ = env.step(action)

                total_reward += reward
                state = next_state

                if done:
                    break

            print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

# Create your custom card game environment
env = CustomCardGameEnv()

# Create a Q-learning agent
agent = QLearningAgent(env)

# Train the agent
agent.train(num_episodes=1000)

# Test the agent
agent.play(num_episodes=10)
