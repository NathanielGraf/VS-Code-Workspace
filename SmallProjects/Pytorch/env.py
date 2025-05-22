import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
#import torchrl
import random
import torch.nn.functional as F
import csv
from itertools import product
import copy



# Path to your CSV file
CSV_PATH = r"C:\Users\natha\OneDrive\Documents\GitHub\VS-Code-Workspace\SmallProjects\Pytorch\PokerHandTable.csv"

def generate_deck():
    return list(product(["H", "S", "C", "D"], range(2, 15)))

def load_hand_rankings(csv_path):
    """
    Loads the hand ranking CSV into a dictionary:
      dict[ (card1, card2, card3, card4, card5, flush_flag) ] = hand_rank
    Assumes each row has 7 columns:
      rank, c1, c2, c3, c4, c5, flush_flag
    """
    lookup = {}
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            # Convert everything to integers
            row_ints = list(map(int, row))
            
            hand_rank  = row_ints[0]      # First column
            cards      = tuple(row_ints[1:6])  # Next 5 columns
            flush_flag = row_ints[6]      # 7th column (0 or 1)
            
            # Store in dictionary:
            # Key is (cards, flush_flag), Value is hand_rank
            lookup[(cards, flush_flag)] = hand_rank
    
    return lookup

default_dict_suits = {"H": 0, "S": 0, "C": 0, "D": 0}
default_dict_values = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

class CardGameEnv:
    def __init__(self):
        
        self.cards = generate_deck()  # Generate a standard deck of cards
        self.reset()
        
        self.hand_lookup = load_hand_rankings(CSV_PATH)
        
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


    def get_action_mask(self):
        
        #Returns a binary mask of length 52 where 1 indicates the card is still in the deck
        mask = [0] * 52
        suit_order = {"H": 0, "D": 13, "C": 26, "S": 39}
        for suit, rank in self.deck:
            index = suit_order[suit] + (rank - 2)
            mask[index] = 1
        return mask

    
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
    
    def is_terminal(self):
        return self.round > 5 or len(self.deck) == 0
    
    def decode_card(self, encoded_card):
        # Assuming 'encoded_cards' is a list of 52 binary values, where 1 indicates the presence of a card and 0 indicates absence
        suit_order = {0: "H", 1: "D", 2: "C", 3: "S"}

        suit = suit_order[encoded_card // 13]
        rank = (encoded_card % 13) + 2  # Add 2 to get the rank, since the smallest rank is 2
                
        return (suit, rank)

    def clone_state(self):
        return {
            "deck": copy.deepcopy(self.deck),
            "player_hand": copy.deepcopy(self.player_hand),
            "opponent_hand": copy.deepcopy(self.opponent_hand),
            "round": self.round,
            "player_suits": copy.deepcopy(self.player_suits),
            "player_values": copy.deepcopy(self.player_values)
        }
        
    def load_state(self, state):
        self.deck = copy.deepcopy(state["deck"])
        self.player_hand = copy.deepcopy(state["player_hand"])
        self.opponent_hand = copy.deepcopy(state["opponent_hand"])
        self.round = state["round"]
        self.player_suits = copy.deepcopy(state["player_suits"])
        self.player_values = copy.deepcopy(state["player_values"])

    def reset(self):
        self.deck = self.shuffle_deck(self.cards.copy())
        self.round = 1
        self.player_hand = []
        self.opponent_hand = []
        
        # Initialize suit and value dictionaries for the player
        self.player_suits = {"H": 0, "S": 0, "C": 0, "D": 0}
        self.player_values = {i: 0 for i in range(2, 15)}  # Values from 2 (lowest) to 14 (Ace)

        return self.get_observation_space()
        
    def step(self, action):
        # The action could be a list of cards (subsets) the agent selects
        # For simplicity, we assume the action is a single card represented by a tuple, e.g., ("H", 10)

        # Check if the deck is empty
        
        done = False

        #print(f"Round {self.round}, Deck size: {len(self.deck)}")
        
        action_subset = []
        for choice in action:
            action_subset.append(self.decode_card(choice))
            
        action_subset = tuple(action_subset)
        
        #print("action:", action)
        #print("deck:", self.deck)
        
        if self.round >= 6:
            # If the game should already have ended, return the current state, 0 reward, True for 'done', and an optional info
            return self.get_observation_space(), 0, True, {}, -1
        
        #print("Action Subset:", action_subset)
        #print("Deck: ", self.deck)

       # Draw from deck until we hit one of our chosen cards or run out of cards
        card_drawn = None
        while self.deck:
            top = self.deck.pop(0)
            if top in action_subset:
                card_drawn = top
                break
            self.opponent_hand.append(top)

        # If we never found a chosen card, or we emptied the deck early (rounds < 5), terminate now
        if card_drawn is None or (not self.deck and self.round < 5):
            reward = self.calculate_reward()
            return self.get_observation_space(), reward, True, {}, 0

        # Otherwise we got our card, add it to the player’s hand and carry on
        self.player_hand.append(card_drawn)
            
        
        
     
        
            

        if self.round == 5: 
            done = True
            while len(self.opponent_hand) < 8:
                self.opponent_hand.append(self.deck.pop(0))
            reward = self.calculate_reward()  # Calculate the reward after the action
            #print("Calculated final reward:", reward)
            if self.check_win_condition():
                return self.get_observation_space(), reward, done, {}, 1
            else:
                return self.get_observation_space(), reward, done, {}, 0
                
        else:
            self.round += 1  # Move to the next round

        return self.get_observation_space(), 0, done, {}, -1
    
    def potential(self, num_simulations=10):
        """
        Approximate P(win | current state) by random rollouts.
        Returns a float in [0,1].
        """
        wins = 0
        for _ in range(num_simulations):
            sim = copy.deepcopy(self)   # snapshot current deck/round/hands
            done = False
            win  = 0

            # play out till terminal
            while not done:
                # pick a random single‐card subset
                mask = sim.get_action_mask()
                avail = [i for i,m in enumerate(mask) if m]
                choice = random.choice(avail)
                # step returns (_, reward, done, _, win_flag)
                _, _, done, _, win_flag = sim.step([choice])
                win = win_flag  # last step’s win_flag

            wins += win

        return wins / num_simulations
        
        

    def calculate_reward(self):
       
        """
        Compute a graded final reward using a tanh transformation based on the hand strength difference.
        Lower strength means a stronger hand.
        """
        player_suits = self._get_suit_dict(self.player_hand)
        player_values = self._get_value_dict(self.player_hand)
        opponent_suits = self._get_suit_dict(self.opponent_hand)
        opponent_values = self._get_value_dict(self.opponent_hand)
        

        
        player_strength = self.get_hand_strength(self.player_hand, player_suits, player_values)
        opponent_strength = self.get_hand_strength(self.opponent_hand, opponent_suits, opponent_values)
        
        diff = opponent_strength - player_strength
        
        max_diff = 7461
        # If opponent_strength - player_strength is positive, player wins by that margin.
        
        reward = np.tanh(diff/max_diff) 
      
        if len(self.player_hand) < 5:
            reward = -1  # Heavy penalty if the player doesn't have enough cards.
        return reward



    # Helper methods to build dictionaries for the current hand:
    def _get_suit_dict(self, hand):
        suits = {"H": 0, "S": 0, "C": 0, "D": 0}
        for card in hand:
            suit, _ = card
            suits[suit] += 1
        return suits

    def _get_value_dict(self, hand):
        values = {i: 0 for i in range(2, 15)}  # 2 to Ace (14)
        for card in hand:
            _, rank = card
            values[rank] += 1
        return values

    
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
            
        
        #player_hand = [('C', 2), ('C', 3), ('C', 4), ('C', 5), ('C', 14)]
        #print("player_hand:", player_hand)
            
        player_strength = self.get_hand_strength(player_hand, player_suits, player_values)
        #opponent_strength = self.get_hand_strength(opponent_hand, opponent_suits, opponent_values)
        
        #print("player_strength:", player_strength)
        
        opponent_strength = self.get_hand_strength(opponent_hand, opponent_suits, opponent_values)
        
        #print("opponent_strength:", opponent_strength)
        
        
        if player_strength < opponent_strength:
            return True
        
        else:
            return False
        #print("opponent_strength:", opponent_strength)
        
        #if player_strength > opponent_strength:
            #return True
        #else:
            #return False
        
    def get_hand_strength(self, hand, suits, values):  
        
        
        if len(hand) < 5:
            return 9999  # Assign a very bad score for weak hands
    
    
        player_holdings = self.straight_flush_check(hand)
        if player_holdings != 0:
            return player_holdings
            
        player_holdings = self.four_of_a_kind_check(values)
        if player_holdings != 0:
            return player_holdings
        
        #Only need to check the house card, since both of them can never have the same house. 
        player_holdings = self.full_house_check(values)
        if player_holdings != 0:
            return player_holdings
            
        
        player_holdings = self.flush_check(suits, hand)
        if player_holdings != 0:
            return player_holdings
                
        
        player_holdings = self.straight_check(values)
        if player_holdings != 0:
            return player_holdings

                
        player_holdings = self.three_of_a_kind_check(values)
        if player_holdings != 0:
            return player_holdings
                
        player_holdings = self.two_pair_check(values)
        if player_holdings != 0:
            return player_holdings
        
        player_holdings = self.pair_check(values)
        if player_holdings != 0:
            return player_holdings
        
        player_holdings = self.high_card_check(values)
        if player_holdings != 0:
            return player_holdings
        
        print("No hand found")
        return 0
    
    def bestfive_to_ranks_tuple(self, bestfive):
        """
        Given a list of 5 cards, e.g.:
            [('S', 14), ('S', 13), ('D', 10), ('C', 9), ('H', 8)],
        return just the ranks sorted in descending order as a tuple, e.g.:
            (14, 13, 10, 9, 8)
        """
        # 1) Extract just the ranks from the cards
        ranks = [card[1] for card in bestfive]
        
        # 2) Sort the ranks descending
        ranks.sort(reverse=True)
        
        # 3) Convert to a tuple (hashable, immutable)
        return tuple(ranks)
       
    def straight_flush_check(self, hand):
        high_card = 0
        counter = 0
        #Check for straight flush
        for i in range(len(hand)-1):
            #print(hand[i][0], hand[i+1][0], hand[i][1], hand[i+1][1])
            
            if hand[i][0] == hand[i+1][0] and hand[i][1] == hand[i+1][1] - 1:
                counter += 1
                
            #Check for the special case of the Ace being the lowest card in the straight
            
            elif counter == 3 and hand[i][0] == hand[i+1][0] and hand[i][1] == 5 and (hand[i][0], 14) in hand:
                high_card = max(high_card, 5)

            else:
                counter = 0
        
            if counter >= 4:
                high_card = max(high_card, hand[i+1][1])
        
        if high_card == 0:
            #print("No Straight Flush")
            return 0
        else:
            #print("Straight Flush", high_card)
            return 15-high_card
        
    def four_of_a_kind_check(self, values):
        high_card = 0
        kicker = 0
        for i in values:
            if values[i] == 4: 
                high_card = max(high_card, i)
                
        for i in values:
            if values[i] >= 1 and i != high_card:        
                kicker = max(kicker, i)
        
        if high_card == 0 or kicker == 0:
            #print("No Four of a Kind")
            return 0
        else:       
            #print("Four of a Kind", high_card)
            #return 11 + 12*(14-high_card) + (14-kicker) - (kicker < high_card)
            besthand = [high_card, high_card, high_card, high_card, kicker]
            besthand.sort(reverse = True)
            rank_tuple = tuple(besthand)
            return self.hand_lookup[(rank_tuple, 0)]
            
    def full_house_check(self, values):
        house_card = 0
        full_card = 0
        for i in values:
            if values[i] >= 3:
                house_card = max(house_card, i)
        
        for i in values:
            if i == house_card:
                continue
            elif values[i] >= 2:
                full_card = max(full_card, i)
        
        if house_card == 0 or full_card == 0:
            #print("No Full House")
            return 0
        else:     
            #return 167 + 12*(14-house_card) + (14-full_card) - (full_card < house_card)
            besthand = [house_card, house_card, house_card, full_card, full_card]
            besthand.sort(reverse = True)
            rank_tuple = tuple(besthand)
            return self.hand_lookup[(rank_tuple, 0)]          

    def flush_check(self, suits, cards):
        
        #Sort descending by value
        cards.sort(reverse = True)
        bestfive = None
        for i in suits:
            if suits[i] >= 5:
                for j in range(len(cards)):
                    if cards[j][0] == i:
                        topfive = cards[j:j+5]
                        if bestfive == None or topfive > bestfive:
                            bestfive = topfive
                       
                        #Break the loop if we find the first card of the suit we are looking for, move to the next suit.
                        break
                
        
        if bestfive == None:
            #print("No Flush")
            return 0
        else:
            ranks_tuple = self.bestfive_to_ranks_tuple(bestfive)
            #print("Flush", high_card)
            return self.hand_lookup[(ranks_tuple, 1)]
        
    def straight_check(self, values):
        #Don't forget to check for the special case of the Ace being the lowest card in the straight
        high_card = 0
        counter = 0
        for i in range(2, 14):
            if values[i] == 1 and values[i+1] == 1 and i != 14:
                counter += 1
                if counter >= 4:
                    high_card = max(high_card, i+1)
            
            #Wheel straight
            elif counter == 3 and values[i] >= 1 and i == 5 and values[14] >= 1:
                high_card = max(high_card, 5)
                
            else:
                counter = 0
                
            
                
        
        if high_card == 0:
            #print("No Straight")
            return 0
        else:
            #print("Straight", high_card)
            return 1600 + (14-high_card)

    def three_of_a_kind_check(self, values):
        high_card = 0
        second = 0
        third = 0
        for i in values:
            if values[i] == 3:
                high_card = max(high_card, i)
        
        for i in values: 
            if values[i] == 1:
                second = max(second, i)
        
        for i in values: 
            if values[i] == 1 and i != second:
                third = max(third, i)
        
        if high_card == 0:
            #print("No Three of a Kind")
            return 0
        else:     
            besthand = [high_card, high_card, high_card, second, third]
            besthand.sort(reverse = True)
            rank_tuple = tuple(besthand)
            return self.hand_lookup[(rank_tuple, 0)]

    def two_pair_check(self, values):
        top_pair = 0
        bottom_pair = 0
        high_card = 0
        for i in values:
            if values[i] == 2:
                top_pair = max(top_pair, i)
        
                
        for i in values: 
            if values[i] == 2 and i != top_pair:
                bottom_pair = max(bottom_pair, i)
        
        for i in values: 
            if values[i] <= 2:
                high_card = max(high_card, i)
        
        if top_pair == 0 or bottom_pair == 0:
            #print("No Two Pair")
            return 0
        else:     
            besthand = [top_pair, top_pair, bottom_pair, bottom_pair, high_card]
            besthand.sort(reverse = True)
            rank_tuple = tuple(besthand)
            return self.hand_lookup[(rank_tuple, 0)]
        
    def pair_check(self, values):
        pair = 0
        one = 0
        two = 0
        three = 0
        for i in values:
            if values[i] == 2:
                pair = max(pair, i)
        
        for i in values:
            if values[i] == 1:
                one = max(one, i)   
                
        for i in values:
            if values[i] == 1 and i != one:
                two = max(two, i)
                
        for i in values:
            if values[i] == 1 and i != one and i != two:
                three = max(three, i)
        
        
        if pair == 0:
            #print("No Pair")
            return 0
        else:     
            besthand = [pair, pair, one, two, three]
            besthand.sort(reverse = True)
            rank_tuple = tuple(besthand)
            return self.hand_lookup[(rank_tuple, 0)]
        
        #Finish fixing the pair and high card functions, add high card tiebreak functionality.
        
    def high_card_check(self, values):
        
        cards = []
        for i in values:
            if values[i] != 0:
                cards.append(i)
                
        cards.sort(reverse = True)
        
        if cards[0] == 0:
            #print("No High Card")
            return 0
        else:     
            besthand = [cards[0], cards[1], cards[2], cards[3], cards[4]]
            besthand.sort(reverse = True)
            rank_tuple = tuple(besthand)
            return self.hand_lookup[(rank_tuple, 0)]
              
        
