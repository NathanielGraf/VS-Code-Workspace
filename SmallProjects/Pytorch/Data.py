import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
#import torchrl
import random
import torch.nn.functional as F
from treys import Card
from treys import Evaluator

class CardGameEnv:
    def __init__(self):
        
        #Create a deck of tuples of cards: 
        self.cards = ['Ah', 'Kh', 'Qh', 'Jh', 'Th', '9h', '8h', '7h', '6h', '5h', '4h', '3h', '2h', 'Ad', 'Kd', 'Qd', 'Jd', 'Td', '9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d', 'Ac', 'Kc', 'Qc', 'Jc', 'Tc', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c', 'As', 'Ks', 'Qs', 'Js', 'Ts', '9s', '8s', '7s', '6s', '5s', '4s', '3s', '2s']
        #self.deck = self.shuffle_deck(self.cards.copy())
        self.reset()
        
    def shuffle_deck(self, deck):
        random.shuffle(deck)
        return deck

    def get_observation_space(self):
        player_hand_encoded = self.encode_cards(self.player_hand)
        opponent_hand_encoded = self.encode_cards(self.opponent_hand)  # Use this only if the opponent's hand is partially/fully observable
        deck_encoded = self.encode_cards(self.deck)

        # Normalize the round number to be between 0 and 1
        max_rounds = 5  # Assuming there are a maximum of 5 rounds in your game
        round_normalized = [self.round / max_rounds]

        # Concatenate all components to form the observation space
        observation = round_normalized + player_hand_encoded + opponent_hand_encoded + deck_encoded
        #print("observation:", observation)
        return observation
    
    def get_action_space(self):
        
        # Example: Encode the action space as a int
        # This is just a placeholder; you'll need to design this based on your neural network's output layer
        action_space = 52  # 52 cards in the deck
        return action_space

    def encode_cards(self, cards):
        # Encodes a list of card strings into a list of indices
        
        # Maps card strings to their indices
        card_to_index = {card: i for i, card in enumerate(self.cards)}

        return [card_to_index[card] for card in cards]

    def decode_cards(self, indexes):
        # Maps indices back to card strings
        index_to_card = {i: card for i, card in enumerate(self.cards)}
        
        # Decodes a single index back into its card string
        return [index_to_card[index] for index in indexes]

    def reset(self):
        self.deck = self.shuffle_deck(self.cards.copy())
        self.round = 0
        self.player_hand = []
        self.opponent_hand = []
        return self.get_observation_space()
        
    def step(self, action):
        # The action could be a list of cards (subsets) the agent selects
        # For simplicity, we assume the action is a single card represented by a tuple, e.g., ("H", 10)
        
        action = self.decode_cards(action)
        
        #print("action:", action)
        #print("deck:", self.deck)
        
        if self.round >= 5:
            # If the game should already have ended, return the current state, 0 reward, True for 'done', and an optional info
            return self.get_observation_space(), 0, True, {}

        # Draw cards from the deck until the chosen card is drawn
        card_drawn = self.deck.pop(0)  # Draw the top card
        #print("deck", self.deck)
        while card_drawn != action:
            self.opponent_hand.append(card_drawn)  # Add the card to the dealer's hand
            if not self.deck:
                observation = self.get_observation_space()
                #print("Deck is empty. Game ended early.")
                return observation, 0, 1, {"message": "Deck is empty. Game ended early."}
            card_drawn = self.deck.pop(0)
        #print("Deck size left", len(self.deck))
        self.player_hand.append(card_drawn)  # Add the selected card to the player's hand
        self.round += 1  # Move to the next round
        
        if not self.deck and self.round < 5:
            # If the deck is empty before the game should have ended, return the current state, 0 reward, True for 'done', and an optional info
            #print("Deck is empty. Game ended early.")
            return self.get_observation_space(), 0, True, {"message": "Deck is empty. Game ended early."}

            

        done = self.round >= 5  # Check if the game is over
        reward = self.calculate_reward(done)  # Calculate the reward after the action

        return self.get_observation_space(), reward, done, {}

    def calculate_reward(self, done):
        # Base reward for completing a round
        reward = 0
        
        # Extra rewards for high-value cards in hand
        #print("player_hand:", self.player_hand)
        for card in self.player_hand:
            suit, rank = card
            if rank > 10:  # Assuming ranks above 10 are considered high-value
                reward += rank - 10  # Reward is proportional to the card's rank
        
        # Penalty for an incomplete hand
        if len(self.player_hand) < 5:
            reward -= 5  # Apply a fixed penalty for not having a full hand

        # Bonus for winning condition
        if done:
            if self.check_win_condition():
                reward += 30  # Assign a large reward for winning
            else:   
                reward -= 30

        return reward
    
    def sort_hand(self, hand):
        sorted_hand = []
        for i in range(len(hand)):
            sorted_hand.append(hand[i])
        sorted_hand.sort()
        return sorted_hand

    def check_win_condition(self):
        # Check if the player's hand is better than the opponent's hand
        
        evaluator = Evaluator()
        player_hand = self.sort_hand(self.player_hand)
        
        
        hand = [Card.new('Ah'), Card.new('Kh'), Card.new('Qh'), Card.new('Jh'), Card.new('Th')]
        board = []
        print(evaluator.evaluate(board, hand))
        
      
            
        winner = self.winner_check(player_hand, opponent_hand, player_suits, player_values, opponent_suits, opponent_values)
        if winner == "Player":
            return True
        else:
            return False
        
    
        
class PolicyNetwork(nn.Module):
    def __init__(self, observation_space, action_space):
        super(PolicyNetwork, self).__init__()
        # Assuming observation_space_size and action_space_size are integers representing the size of the input and output layers
        self.fc1 = nn.Linear(157, 128)  # First fully connected layer, 157 for the observation space
        self.fc2 = nn.Linear(128, 256)  # Second fully connected layer
        self.fc3 = nn.Linear(256, 128)  # Third fully connected layer
        self.action_head = nn.Linear(128, 52)  # Output layer for actions, 52 for the action space
        self.value_head = nn.Linear(128, 1)  # Output layer for state value, useful for actor-critic methods

    def forward(self, x):
        # Forward pass through the network
        x = F.relu(self.fc1(x))  # Activation function for first layer
        x = F.relu(self.fc2(x))  # Activation function for second layer
        x = F.relu(self.fc3(x))  # Activation function for third layer
        #print("actionhead", self.action_head(x))
        #print("action_probs", F.softmax(self.action_head(x), dim=-1))
        
        raw_action_logits = self.action_head(x)
        stabilized_logits = raw_action_logits - raw_action_logits.max(dim=1, keepdim=True).values
        action_probs = F.softmax(stabilized_logits, dim=-1)  # Softmax on the action head for action probabilities
        state_values = self.value_head(x)  # State value from value head
        return action_probs, state_values

    def train(env, policy_network, episodes, optimizer, gamma=0.99):
        
        win_count = 0
        win_rates = []
        
        for i in range(episodes):
            
            
            
            if (i + 1) % 100 == 0:
                print(f"Episode {i + 1}/{episodes}")
                win_rate = win_count / 100
                win_rates.append(win_rate)
                win_count = 0  # Reset for the next batch of 100 games
            
            state = env.reset()
            done = False
            while not done:
                
                # Ensure state is a torch Tensor
                state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Add a batch dimension
                
                #print("state_tensor shape:", state_tensor.shape)
                #print("state_tensor:", state_tensor)
                
                # Convert state to tensor and get action probabilities and value estimate
                action_probs, state_value = policy_network(state_tensor)
                
                
                #print("action_probs:", action_probs)
                
                #Need to add this prob before masking so we don't underflow, this will still be masked so we don't select unavailable cards.
                action_probs = action_probs + 1e-35
                
                #Looks good
                #print("action_probs shape:", action_probs.shape)
                #print("edited_action_probs:", action_probs)
                
                #print("state_tensor shape:", state_tensor.shape)
                #print("state_tensor:", state_tensor)
                
                #print("state_value shape:", state_value.shape)
                #print("state_value:", state_value)
                
                
                
                # Get a binary mask where 1 indicates the card is still in the deck
                deck_state = state[-52:]  # Assuming the last 52 elements of the state represent the deck
                mask = torch.FloatTensor(deck_state).unsqueeze(0)
                
                #print("mask", mask)

                # Apply the mask to action probabilities
                masked_action_probs = action_probs * mask
                
                # Define a small constant, ensuring it's of the same dtype as masked_action_probs
                #epsilon = torch.tensor(1e-20, dtype=masked_action_probs.dtype, device=masked_action_probs.device)


                #print("masked_action_probs shape:", masked_action_probs.shape)
                #print("masked_action_probs:", masked_action_probs)
                
                
                
                # Re-normalize the masked action probabilities
                # Assuming 'logits' is the raw output from a network layer
                

                # Apply softmax to get normalized probabilities
                
                normalized_action_probs = (masked_action_probs) / (masked_action_probs.sum())

                
                #print("Sum of probabilities (with epsilon):", masked_action_probs.sum())
                #print("Normalized action probabilities:", normalized_action_probs)
                
                #print("normalized_action_probs shape:", normalized_action_probs.shape)
                #print("normalized_action_probs:", normalized_action_probs)
                
                # Sample an action based on the masked and normalized probabilities
                action = torch.multinomial(normalized_action_probs, 1).item()
                
                #print("action:", action)
                
                
                # Take action in the environment
                next_state, reward, done, _ = env.step(action)
                
                #Ensure next_state is also a torch Tensor
                next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)  # Add a batch dimension
                
                # Compute advantage and update network
                _, next_state_value = policy_network(next_state_tensor)
                advantage = reward + (1 - done) * gamma * next_state_value - state_value
                
                # Compute loss (actor loss + critic loss)
                actor_loss = -torch.log(action_probs[0, action]) * advantage.detach() # Detach advantage to stop gradients
  
                critic_loss = advantage.pow(2)
                loss = actor_loss + critic_loss
                
                # Backpropagate and update network weights
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                state = next_state
            if done:
                if reward > 0:
                    win_count += 1
        
        print("Training complete.")
        print("Win rates:", win_rates)


# Initialize your environment and policy network
env = CardGameEnv()
observation_space = env.get_observation_space()
action_space = env.get_action_space()
policy_network = PolicyNetwork(observation_space, action_space)
optimizer = optim.Adam(policy_network.parameters(), lr=1e-3)

# Train the agent
PolicyNetwork.train(env, policy_network, episodes=10000, optimizer=optimizer)
