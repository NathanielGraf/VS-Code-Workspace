import numpy as np
import random
import tensorflow as tf  # or any deep learning library
import custom_env

class DQNAgent:
    def __init__(self, env, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01, learning_rate=0.001, discount_factor=0.99):
        self.env = env
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_network = self.build_q_network()
        self.target_network = self.build_q_network()
        self.replay_buffer = []  # Experience replay buffer
        self.batch_size = 100  # Mini-batch size 32

        #Create input_shape:
        
        input_shape = 105
        
        # Initialize the models with dummy data to create weights
        dummy_input = np.zeros((1, input_shape))  # Replace with your actual input shape
        self.q_network(dummy_input)
        self.target_network(dummy_input)

    def build_q_network(self):
        model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(105,)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(52, activation='linear')  # Output layer with one output neuron per action
    ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
                      loss='mean_squared_error')
        return model

    def choose_action(self, state):

        if np.random.rand() <= self.epsilon:
            return self.env.action_space.sample()  # Explore
        else:
            q_values = self.q_network.predict(np.array([state]))[0]
            #print("Array:", np.array([state]))
            
            #print("QValues:", q_values)
            
            # Apply epsilon-greedy to select multiple cards
            num_cards_to_choose = np.random.randint(1, len(q_values) + 1)  # Choose 1 to len(q_values) cards
            chosen_cards = np.argsort(q_values)[-num_cards_to_choose:]  # Choose the cards with the highest Q-values
            
            binary_action = np.zeros(len(q_values), dtype=int)  # Ensure the array is of integer type
            binary_action[chosen_cards] = 1  # Set the chosen card positions to 1
            
            # Ensure at least one card is chosen
            if np.sum(binary_action) == 0:
                binary_action[np.random.choice(len(q_values))] = 1
            
            return binary_action

        
    def update_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.replay_buffer) < self.batch_size:
            return

        # Sample a mini-batch from the replay buffer
        mini_batch = random.sample(self.replay_buffer, self.batch_size)
        print("Mini Batch:", mini_batch)

        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target += self.discount_factor * np.max(self.target_network.predict(np.array([next_state]))[0])

            target_q_values = self.q_network.predict(np.array([state]))
            target_q_values[0][action] = target

            self.q_network.fit(np.array([state]), target_q_values, epochs=1, verbose=0)

    #Maybe add reward thing for improving poker hand 

    def update_target_network(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def play(self, num_episodes):
        win_count = 0
        for episode in range(num_episodes):
            state = env.reset()
            total_reward = 0
            episode_buffer = []  # Create an empty buffer for this episode

            while True:
                action = self.choose_action(state)
                result = env.step(action)
                next_state = np.array(result['next_state'])
                reward = result['reward']
                done = result['done']
                total_reward += reward

                # Append the experience to the episode buffer
                episode_buffer.append((state, action, reward, next_state, done))

                if done:
                    # Calculate the final reward based on the episode outcome
                    final_reward = 1.0 if total_reward > 0 else -1.0  # Adjust based on your game's rules

                    # Update the rewards in the episode buffer with the final reward
                    for i in range(len(episode_buffer)):
                        s, a, _, ns, _ = episode_buffer[i]
                        episode_buffer[i] = (s, a, final_reward, ns, done)

                    # Add the experiences in the episode buffer to the replay buffer
                    self.replay_buffer.extend(episode_buffer)

                    if total_reward > 0:
                        win_count += 1
                    break

                state = next_state  # Update the current state

            print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")
            self.update_epsilon()
            self.update_target_network()

        print(f"Win rate: {win_count / num_episodes * 100:.2f}%")


# Create your custom card game environment
env = custom_env.CustomCardGameEnv()

# Create a DQN agent
agent = DQNAgent(env)

# Train the agent
agent.train()

# Test the agent
agent.play(num_episodes=100)

#Print("Replay Buffer:", agent.replay_buffer)
