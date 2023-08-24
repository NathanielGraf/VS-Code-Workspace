cards = [["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11], ["H", 12], ["H", 13], ["H", 14], ["S", 2], ["S", 3], ["S", 4], ["S", 5], ["S", 6], ["S", 7], ["S", 8], ["S", 9], ["S", 10], ["S", 11], ["S", 12], ["S", 13], ["S", 14], ["C", 2], ["C", 3], ["C", 4], ["C", 5], ["C", 6], ["C", 7], ["C", 8], ["C", 9], ["C", 10], ["C", 11], ["C", 12], ["C", 13], ["C", 14], ["D", 2], ["D", 3], ["D", 4], ["D", 5], ["D", 6], ["D", 7], ["D", 8], ["D", 9], ["D", 10], ["D", 11], ["D", 12], ["D", 13], ["D", 14]]
default_dict_suits = {"H": 0, "S": 0, "C": 0, "D": 0}
default_dict_values = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

card_to_index_dict = {["H", 2]: 0, ["H", 3]: 1, ["H", 4]: 2, ["H", 5]: 3, ["H", 6]: 4, ["H", 7]: 5, ["H", 8]: 6, ["H", 9]: 7, ["H", 10]: 8, ["H", 11]: 9, ["H", 12]: 10, ["H", 13]: 11, ["H", 14]: 12, ["S", 2]: 13, ["S", 3]: 14, ["S", 4]: 15, ["S", 5]: 16, ["S", 6]: 17, ["S", 7]: 18, ["S", 8]: 19, ["S", 9]: 20, ["S", 10]: 21, ["S", 11]: 22, ["S", 12]: 23, ["S", 13]: 24, ["S", 14]: 25, ["C", 2]: 26, ["C", 3]: 27, ["C", 4]: 28, ["C", 5]: 29, ["C", 6]: 30, ["C", 7]: 31, ["C", 8]: 32, ["C", 9]: 33, ["C", 10]: 34, ["C", 11]: 35, ["C", 12]: 36, ["C", 13]: 37, ["C", 14]: 38, ["D", 2]: 39, ["D", 3]: 40, ["D", 4]: 41, ["D", 5]: 42, ["D", 6]: 43, ["D", 7]: 44, ["D", 8]: 45, ["D", 9]: 46, ["D", 10]: 47, ["D", 11]: 48, ["D", 12]: 49, ["D", 13]: 50, ["D", 14]: 51}
index_to_card_dict = {0: ["H", 2], 1: ["H", 3], 2: ["H", 4], 3: ["H", 5], 4: ["H", 6], 5: ["H", 7], 6: ["H", 8], 7: ["H", 9], 8: ["H", 10], 9: ["H", 11], 10: ["H", 12], 11: ["H", 13], 12: ["H", 14], 13: ["S", 2], 14: ["S", 3], 15: ["S", 4], 16: ["S", 5], 17: ["S", 6], 18: ["S", 7], 19: ["S", 8], 20: ["S", 9], 21: ["S", 10], 22: ["S", 11], 23: ["S", 12], 24: ["S", 13], 25: ["S", 14], 26: ["C", 2], 27: ["C", 3], 28: ["C", 4], 29: ["C", 5], 30: ["C", 6], 31: ["C", 7], 32: ["C", 8], 33: ["C", 9], 34: ["C", 10], 35: ["C", 11], 36: ["C", 12], 37: ["C", 13], 38: ["C", 14], 39: ["D", 2], 40: ["D", 3], 41: ["D", 4], 42: ["D", 5], 43: ["D", 6], 44: ["D", 7], 45: ["D", 8], 46: ["D", 9], 47: ["D", 10], 48: ["D", 11], 49: ["D", 12], 50: ["D", 13], 51: ["D", 14]}

round_array = [-1, -1, -1, -1, -1]

wanted_subset = []
for i in range (0, 52):
    wanted_subset.append(-1)

player_indexes = []
for i in range (0, 52):
    player_indexes.append(-1)
    
opponent_indexes = []
for i in range (0, 52):
    opponent_indexes.append(-1)
    
remaining_indexes = []
for i in range (0, 52):
    remaining_indexes.append(i)

import random

def shuffle(deck):
    #Deep copy the cards list so that the original is not modified:
    newcards = []
    for i in range(len(deck)):
        newcards.append(deck[i])
    
    #Shuffle the deck:  
    random.shuffle(newcards)
    return newcards

def sort_hand(hand):
    sorted_hand = []
    for i in range(len(hand)):
        sorted_hand.append(hand[i])
    sorted_hand.sort()
    return sorted_hand

def main():
    deck = shuffle(cards)
    
    player_hand = []
    opponent_hand = []
    
    for round_num in range(1, 6):
        round_array[round_num-1] = 1
        #wanted_subset = SubsetFinder(player_indexes, opponent_indexes, remaining_indexes, round_array) 
        play_round(player_hand, opponent_hand, deck, wanted_subset)
        
        round_array[round_num-1] = -1
        
    while len(opponent_hand) < 8:
        opponent_hand.append(deck.pop())
        
    #Winner checker: 
    player_hand = sort_hand(player_hand)
    opponent_hand = sort_hand(opponent_hand)
    
    #Create the dicts for the player's hands:
    player_suits = default_dict_suits.copy()
    player_values = default_dict_values.copy()
    opponent_suits = default_dict_suits.copy()
    opponent_values = default_dict_values.copy()
    
    #Fill the dicts with the values from the player's hands:
    for i in range(len(player_hand)):
        player_suits[player_hand[i][0]] += 1
        player_values[player_hand[i][1]] += 1
    
    for i in range(len(opponent_hand)):
        opponent_suits[opponent_hand[i][0]] += 1
        opponent_values[opponent_hand[i][1]] += 1
        
    winner = winner_check(player_hand, opponent_hand, player_suits, player_values, opponent_suits, opponent_values)
    return winner
    
    
    
    
def play_round(player_hand, opponent_hand, deck, subset):
    
    card_subset = []
    # Player selects a subset of cards
        # To be implemented based on your strategy
    for i, card in enumerate(subset):
        if card == 1:
            card_subset.append(index_to_card_dict[i])
        
    
    # Draw cards until one appears in the player's subset
    while True and len(deck) > 0:
        card = deck.pop()
        if card in card_subset:
            player_hand.append(card)
            break
        opponent_hand.append(card)
    
    for i in player_hand: 
        player_indexes[card_to_index_dict[i]] = 1
        remaining_indexes[card_to_index_dict[i]] = -1
    
    for i in opponent_hand:
        opponent_indexes[card_to_index_dict[i]] = 1
        remaining_indexes[card_to_index_dict[i]] = -1

    
    return()
    
def winner_check(player_hand, opponent_hand, player_suits, player_values, opponent_suits, opponent_values):  
    player_holdings = straight_flush_check(player_hand)
    opponent_holdings = straight_flush_check(opponent_hand)
    if player_holdings != 0 or opponent_holdings != 0:
        if player_holdings > opponent_holdings:
            winner = "Player"
            return winner
        else:
            winner = "Opponent"
            return winner
    
    player_holdings = four_of_a_kind_check(player_hand)
    opponent_holdings = four_of_a_kind_check(opponent_hand)
    if player_holdings != 0 or opponent_holdings != 0:
        if player_holdings > opponent_holdings:
            winner = "Player"
            return winner
        else:
            winner = "Opponent"
            return winner
    
    #Only need to check the house card, since both of them can never have the same house. 
    player_holdings = full_house_check(player_hand)
    opponent_holdings = full_house_check(opponent_hand)
    if player_holdings != 0 or opponent_holdings != 0:
        if player_holdings > opponent_holdings:
            winner = "Player"
            return winner
        else:
            winner = "Opponent"
            return winner
        
    
    player_holdings = flush_check(player_suits, player_hand)
    opponent_holdings = flush_check(opponent_suits, opponent_hand)
    if player_holdings != 0 or opponent_holdings != 0:
        if player_holdings > opponent_holdings:
            winner = "Player"
            return winner
        else:
            winner = "Opponent"
            return winner
            
    
    player_holdings = straight_check(player_hand)
    opponent_holdings = straight_check(opponent_hand)
    if player_holdings != 0 or opponent_holdings != 0:
        if player_holdings > opponent_holdings:
            winner = "Player"
            return winner
        else:
            winner = "Opponent"
            return winner

            
    player_holdings = three_of_a_kind_check(player_values)
    opponent_holdings = three_of_a_kind_check(opponent_values)
    if player_holdings != 0 or opponent_holdings != 0:
        if player_holdings > opponent_holdings:
            winner = "Player"
            return winner
        else:
            winner = "Opponent"
            return winner
            
    player_holdings = two_pair_check(player_values)
    opponent_holdings = two_pair_check(opponent_values)
    
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
    
    player_holdings = pair_check(player_values)
    opponent_holdings = pair_check(opponent_values)
    
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
    
    
    player_holdings = high_card_check(player_values)
    opponent_holdings = high_card_check(opponent_values)
    
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
    
def straight_flush_check(hand):
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
    
def four_of_a_kind_check(values):
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
        
def full_house_check(values):
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
    
def flush_check(suits, cards):
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
    
def straight_check(hand):
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

def three_of_a_kind_check(values):
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

def two_pair_check(values):
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

def pair_check(values):
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

wincount = 0
runs = 100000
for i in range(runs):
    if main() == "Player":
        wincount += 1
    
print(wincount/runs)




