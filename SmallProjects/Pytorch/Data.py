import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
#import torchrl
import random
import torch.nn.functional as F



default_dict_suits = {"H": 0, "S": 0, "C": 0, "D": 0}
default_dict_values = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
hearts = [["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11], ["H", 12], ["H", 13], ["H", 14]]
clubs = [["C", 2], ["C", 3], ["C", 4], ["C", 5], ["C", 6], ["C", 7], ["C", 8], ["C", 9], ["C", 10], ["C", 11], ["C", 12], ["C", 13], ["C", 14]]
spades = [["S", 2], ["S", 3], ["S", 4], ["S", 5], ["S", 6], ["S", 7], ["S", 8], ["S", 9], ["S", 10], ["S", 11], ["S", 12], ["S", 13], ["S", 14]]
diamonds = [["D", 2], ["D", 3], ["D", 4], ["D", 5], ["D", 6], ["D", 7], ["D", 8], ["D", 9], ["D", 10], ["D", 11], ["D", 12], ["D", 13], ["D", 14]]

class CardGameEnv:
    def __init__(self):
        #self.cards = [["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11], ["H", 12], ["H", 13], ["H", 14], ["S", 2], ["S", 3], ["S", 4], ["S", 5], ["S", 6], ["S", 7], ["S", 8], ["S", 9], ["S", 10], ["S", 11], ["S", 12], ["S", 13], ["S", 14], ["C", 2], ["C", 3], ["C", 4], ["C", 5], ["C", 6], ["C", 7], ["C", 8], ["C", 9], ["C", 10], ["C", 11], ["C", 12], ["C", 13], ["C", 14], ["D", 2], ["D", 3], ["D", 4], ["D", 5], ["D", 6], ["D", 7], ["D", 8], ["D", 9], ["D", 10], ["D", 11], ["D", 12], ["D", 13], ["D", 14]]
        
        #Create a deck of tuples of cards: 
        self.cards = [("H", 2), ("H", 3), ("H", 4), ("H", 5), ("H", 6), ("H", 7), ("H", 8), ("H", 9), ("H", 10), ("H", 11), ("H", 12), ("H", 13), ("H", 14), ("S", 2), ("S", 3), ("S", 4), ("S", 5), ("S", 6), ("S", 7), ("S", 8), ("S", 9), ("S", 10), ("S", 11), ("S", 12), ("S", 13), ("S", 14), ("C", 2), ("C", 3), ("C", 4), ("C", 5), ("C", 6), ("C", 7), ("C", 8), ("C", 9), ("C", 10), ("C", 11), ("C", 12), ("C", 13), ("C", 14), ("D", 2), ("D", 3), ("D", 4), ("D", 5), ("D", 6), ("D", 7), ("D", 8), ("D", 9), ("D", 10), ("D", 11), ("D", 12), ("D", 13), ("D", 14)]
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
        # Assuming 'cards' is a list of tuples like [("H", 10), ("D", 3)], where the first element is the suit and the second is the rank
        # The deck is a standard 52-card deck
        encoded = [0] * 52  # 52 cards in a standard deck
        suit_order = {"H": 0, "D": 13, "C": 26, "S": 39}  # Assign each suit a starting index
        for card in cards:
            suit, rank = card
            index = suit_order[suit] + (rank - 2)  # Subtract 2 because the smallest rank is 2, not 0
            encoded[index] = 1
        return encoded
    
    def decode_card(self, encoded_card):
        # Assuming 'encoded_cards' is a list of 52 binary values, where 1 indicates the presence of a card and 0 indicates absence
        suit_order = {0: "H", 1: "D", 2: "C", 3: "S"}
        

            
        suit = suit_order[encoded_card // 13]
        rank = (encoded_card % 13) + 2  # Add 2 to get the rank, since the smallest rank is 2
               
                
        return (suit, rank)

    def reset(self):
        self.deck = self.shuffle_deck(self.cards.copy())
        self.round = 0
        self.player_hand = []
        self.opponent_hand = []
        return self.get_observation_space()
        
    def step(self, action):
        # The action could be a list of cards (subsets) the agent selects
        # For simplicity, we assume the action is a single card represented by a tuple, e.g., ("H", 10)

        # Check if the deck is empty
   
        
        
        action = self.decode_card(action)
        
        print("action:", action)
        print("deck:", self.deck)
        
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
        
        player_hand = self.player_hand.copy()
        
        
        opponent_hand = self.opponent_hand.copy()   
        player_hand = self.sort_hand(player_hand)
        opponent_hand = self.sort_hand(opponent_hand)
    
        #Create the dicts for the player's hands:
        player_suits = default_dict_suits.copy()
        player_values = default_dict_values.copy()
    
        opponent_suits = default_dict_suits.copy()
        opponent_values = default_dict_values.copy()
        
        #Fill the dicts with the values from the player's hands:
        #print("player_hand:", player_hand)
        for i in range(len(player_hand)):
            player_suits[player_hand[i][0]] += 1
            player_values[player_hand[i][1]] += 1
            
        #print("player_values:", player_values)
        
        for i in range(len(opponent_hand)):
            opponent_suits[opponent_hand[i][0]] += 1
            opponent_values[opponent_hand[i][1]] += 1
            
        winner = self.winner_check(player_hand, opponent_hand, player_suits, player_values, opponent_suits, opponent_values)
        if winner == "Player":
            return True
        else:
            return False
        
    def winner_check(self, player_hand, opponent_hand, player_suits, player_values, opponent_suits, opponent_values):  
        player_holdings = self.straight_flush_check(player_hand)
        opponent_holdings = self.straight_flush_check(opponent_hand)
        if player_holdings != 0 or opponent_holdings != 0:
            if player_holdings > opponent_holdings:
                winner = "Player"
                return winner
            else:
                winner = "Opponent"
                return winner
        
        player_holdings = self.four_of_a_kind_check(player_values)
        opponent_holdings = self.four_of_a_kind_check(opponent_values)
        if player_holdings != 0 or opponent_holdings != 0:
            if player_holdings > opponent_holdings:
                winner = "Player"
                return winner
            else:
                winner = "Opponent"
                return winner
        
        #Only need to check the house card, since both of them can never have the same house. 
        player_holdings = self.full_house_check(player_values)
        opponent_holdings = self.full_house_check(opponent_values)
        if player_holdings != 0 or opponent_holdings != 0:
            if player_holdings > opponent_holdings:
                winner = "Player"
                return winner
            else:
                winner = "Opponent"
                return winner
            
        
        player_holdings = self.flush_check(player_suits, player_hand)
        opponent_holdings = self.flush_check(opponent_suits, opponent_hand)
        if player_holdings != 0 or opponent_holdings != 0:
            if player_holdings > opponent_holdings:
                winner = "Player"
                return winner
            else:
                winner = "Opponent"
                return winner
                
        
        player_holdings = self.straight_check(player_hand)
        opponent_holdings = self.straight_check(opponent_hand)
        if player_holdings != 0 or opponent_holdings != 0:
            if player_holdings > opponent_holdings:
                winner = "Player"
                return winner
            else:
                winner = "Opponent"
                return winner

                
        player_holdings = self.three_of_a_kind_check(player_values)
        opponent_holdings = self.three_of_a_kind_check(opponent_values)
        if player_holdings != 0 or opponent_holdings != 0:
            if player_holdings > opponent_holdings:
                winner = "Player"
                return winner
            else:
                winner = "Opponent"
                return winner
                
        player_holdings = self.two_pair_check(player_values)
        opponent_holdings = self.two_pair_check(opponent_values)
        
        if player_holdings[0] != 0 or opponent_holdings[0] != 0:
            if player_holdings[0] > opponent_holdings[0]:
                winner = "Player"
                
            elif player_holdings[0] == opponent_holdings[0]:
                if player_holdings[1] > opponent_holdings[1]:
                    winner = "Player"
                elif player_holdings[1] == opponent_holdings[1]:
                    if player_holdings[2] > opponent_holdings[2]:
                        winner = "Player"
                    else:
                        winner = "Opponent"
                
                else:
                    winner = "Opponent"
                    
            
            else:
                winner = "Opponent"
        
        player_holdings = self.pair_check(player_values)
        opponent_holdings = self.pair_check(opponent_values)
        
        if player_holdings[0] != 0 or opponent_holdings[0] != 0:
            if player_holdings[0] > opponent_holdings[0]:
                winner = "Player"
                
            elif player_holdings[0] == opponent_holdings[0]:
                if player_holdings[1] > opponent_holdings[1]:
                    winner = "Player"
                elif player_holdings[1] == opponent_holdings[1]:
                    if player_holdings[2] > opponent_holdings[2]:
                        winner = "Player"
                    elif player_holdings[2] == opponent_holdings[2]:
                        if player_holdings[3] > opponent_holdings[3]:
                            winner = "Player"
                        else:
                            winner = "Opponent"
                    else:
                        winner = "Opponent"
                
                else:
                    winner = "Opponent"
            
            else:
                winner = "Opponent"
        
        
        player_holdings = self.high_card_check(player_values)
        opponent_holdings = self.high_card_check(opponent_values)
        
        if player_holdings[0] != 0 or opponent_holdings[0] != 0:
            if player_holdings[0] > opponent_holdings[0]:
                winner = "Player"
                
            elif player_holdings[0] == opponent_holdings[0]:
                if player_holdings[1] > opponent_holdings[1]:
                    winner = "Player"
                elif player_holdings[1] == opponent_holdings[1]:
                    if player_holdings[2] > opponent_holdings[2]:
                        winner = "Player"
                    elif player_holdings[2] == opponent_holdings[2]:
                        if player_holdings[3] > opponent_holdings[3]:
                            winner = "Player"
                        elif player_holdings[3] == opponent_holdings[3]:
                            if player_holdings[4] > opponent_holdings[4]:
                                winner = "Player"
                            else:
                                winner = "Opponent"
                        else:
                            winner = "Opponent"
                    else:
                        winner = "Opponent"
                
                else:
                    winner = "Opponent"
            
            else:
                winner = "Opponent"
        
    def straight_flush_check(self, hand):
        high_card = 0
        counter = 0
        for i in range(len(hand)-1):
            
            if hand[i][0] == hand[i+1][0] and hand[i][1] == hand[i+1][1] - 1:
                counter += 1

            else:
                counter = 0
        
            if counter >= 4:
                high_card = max(high_card, hand[i+1][1])
                
        
        if high_card == 0:
            #print("No Straight Flush")
            return 0
        else:
            #print("Straight Flush", high_card)
            return high_card
        
    def four_of_a_kind_check(self, values):
        high_card = 0
        for i in values:
            if values[i] == 4:
                high_card = i
        
        if high_card == 0:
            #print("No Four of a Kind")
            return 0
        else:     
            #print("Four of a Kind", high_card)
            return high_card
            
    def full_house_check(self, values):
        house_card = 0
        full_card = 0
        for i in values:
            if values[i] >= 3:
                house_card = i
        
        for i in values:
            if i == house_card:
                continue
            elif values[i] >= 2:
                full_card = i
        
        if house_card == 0 or full_card == 0:
            #print("No Full House")
            return 0
            
        else:     
            #print("Full House", house_card, "full of", full_card)
            return house_card
        
    def flush_check(self, suits, cards):
        high_card = 0
        for i in suits:
            if suits[i] >= 5:
                flush_high_card = 0
                for j in range(len(cards)):
                    if cards[j][0] == i:
                        flush_high_card = max(flush_high_card, cards[j][1])
                high_card = max(high_card, flush_high_card)
        
        if high_card == 0:
            #print("No Flush")
            return 0
        else:
            #print("Flush", high_card)
            return high_card
        
    def straight_check(self, hand):
        high_card = 0
        counter = 0
        for i in range(len(hand)-1):
            
            if hand[i][1] == hand[i+1][1] - 1:
                counter += 1

            else:
                counter = 0
        
            if counter >= 4:
                high_card = max(high_card, hand[i+1][1])
                
        
        if high_card == 0:
            #print("No Straight")
            return 0
        else:
            #print("Straight", high_card)
            return high_card

    def three_of_a_kind_check(self, values):
        high_card = 0
        for i in values:
            if values[i] == 3:
                high_card = i
        
        if high_card == 0:
            #print("No Three of a Kind")
            return 0
        else:     
            #print("Three of a Kind", high_card)
            return high_card

    def two_pair_check(self, values):
        top_pair = 0
        bottom_pair = 0
        for i in values:
            if values[i] >= 2:
                top_pair = i
                
        for i in values:
            if values[i] >= 2 and i != top_pair:
                bottom_pair = i
        
        for i in values: 
            if values[i] <= 2 and i != top_pair and i != bottom_pair: 
                high_card = i
        
        if top_pair == 0 or bottom_pair == 0:
            #print("No Two Pair")
            return [0, 0, 0]
        else:     
            #print("Two Pair", top_pair, "and", bottom_pair)
            return [top_pair, bottom_pair, high_card]

    def pair_check(self, values):
        high_card = 0
        for i in values:
            if values[i] >= 2:
                high_card = i
        
        for i in values:
            if values[i] == 1 and i != high_card:
                one = i
                
        for i in values:
            if values[i] == 1 and i != high_card and i != one:
                two = i
                
        for i in values:
            if values[i] == 1 and i != high_card and i != one and i != two:
                three = i
        
        
        
        if high_card == 0:
            #print("No Pair")
            return [0, 0, 0, 0]
        else:     
            #print("Pair", high_card)
            return [high_card, one, two, three]
        
        #Finish fixing the pair and high card functions, add high card tiebreak functionality.
        
    def high_card_check(values):
        high_card = 0
        for i in values:
            if values[i] == 1:
                one = i
                
        for i in values:
            if values[i] == 1 and i != one:
                two = i
                
        for i in values:
            if values[i] == 1  and i != one and i != two:
                three = i
                
        for i in values:
            if values[i] == 1 and i != one and i != two and i != three :
                four = i
                
        for i in values:
            if values[i] == 1 and i != one and i != two and i != three and i != four:
                five = i
        
        if high_card == 0:
            #print("No High Card")
            return [0,0,0,0,0]
        else:     
            #print("High Card", high_card)
            return [one, two, three, four, five]
            
        
        
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
        print("actionhead", self.action_head(x))
        print("action_probs", F.softmax(self.action_head(x), dim=-1))
        
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
                
                print("state_tensor shape:", state_tensor.shape)
                print("state_tensor:", state_tensor)
                
                # Convert state to tensor and get action probabilities and value estimate
                action_probs, state_value = policy_network(state_tensor)
                
                #Looks good
                print("action_probs shape:", action_probs.shape)
                print("action_probs:", action_probs)
                
                #print("state_tensor shape:", state_tensor.shape)
                #print("state_tensor:", state_tensor)
                
                #print("state_value shape:", state_value.shape)
                #print("state_value:", state_value)
                
                
                
                # Get a binary mask where 1 indicates the card is still in the deck
                deck_state = state[-52:]  # Assuming the last 52 elements of the state represent the deck
                mask = torch.FloatTensor(deck_state).unsqueeze(0)
                
                print("mask", mask)

                # Apply the mask to action probabilities
                masked_action_probs = action_probs * mask
                
                # Define a small constant, ensuring it's of the same dtype as masked_action_probs
                epsilon = torch.tensor(1e-20, dtype=masked_action_probs.dtype, device=masked_action_probs.device)


                print("masked_action_probs shape:", masked_action_probs.shape)
                print("masked_action_probs:", masked_action_probs)
                
                
                
                # Re-normalize the masked action probabilities
                # Assuming 'logits' is the raw output from a network layer
                

                # Apply softmax to get normalized probabilities
                
                normalized_action_probs = (masked_action_probs) / (masked_action_probs.sum() + epsilon)

                
                print("Sum of probabilities (with epsilon):", masked_action_probs.sum())
                print("Normalized action probabilities:", normalized_action_probs)
                
                #print("normalized_action_probs shape:", normalized_action_probs.shape)
                #print("normalized_action_probs:", normalized_action_probs)
                
                # Sample an action based on the masked and normalized probabilities
                action = torch.multinomial(normalized_action_probs, 1).item()
                
                print("action:", action)
                
                
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
