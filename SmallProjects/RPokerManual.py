cards = [["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11], ["H", 12], ["H", 13], ["H", 14], ["S", 2], ["S", 3], ["S", 4], ["S", 5], ["S", 6], ["S", 7], ["S", 8], ["S", 9], ["S", 10], ["S", 11], ["S", 12], ["S", 13], ["S", 14], ["C", 2], ["C", 3], ["C", 4], ["C", 5], ["C", 6], ["C", 7], ["C", 8], ["C", 9], ["C", 10], ["C", 11], ["C", 12], ["C", 13], ["C", 14], ["D", 2], ["D", 3], ["D", 4], ["D", 5], ["D", 6], ["D", 7], ["D", 8], ["D", 9], ["D", 10], ["D", 11], ["D", 12], ["D", 13], ["D", 14]]
default_dict_suits = {"H": 0, "S": 0, "C": 0, "D": 0}
default_dict_values = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
hearts = [["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11], ["H", 12], ["H", 13], ["H", 14]]
clubs = [["C", 2], ["C", 3], ["C", 4], ["C", 5], ["C", 6], ["C", 7], ["C", 8], ["C", 9], ["C", 10], ["C", 11], ["C", 12], ["C", 13], ["C", 14]]
spades = [["S", 2], ["S", 3], ["S", 4], ["S", 5], ["S", 6], ["S", 7], ["S", 8], ["S", 9], ["S", 10], ["S", 11], ["S", 12], ["S", 13], ["S", 14]]
diamonds = [["D", 2], ["D", 3], ["D", 4], ["D", 5], ["D", 6], ["D", 7], ["D", 8], ["D", 9], ["D", 10], ["D", 11], ["D", 12], ["D", 13], ["D", 14]]

#Data:
#0.34051 for 1000000 runs of the RF 10 up chase.

'''
Elements: 
5 for which round we are on 
52 for which cards the player has 
52 for which cards the opponent has
52 for which cards are left in the deck
'''
import random

def shuffle(deck):
    #Deep copy the cards list so that the original is not modified:
    newcards = []
    for i in range(len(deck)):
        newcards.append(deck[i])
    
    #Shuffle the deck:  
    random.shuffle(newcards)
    return newcards

def deal(cards):
    hand = []
    for i in range(5):
        hand.append(cards.pop())
    return hand

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
    
    #Straight chase implementation:
    #Attempt to get a straight with our 5 cards:

    # do 5-10 for first subset:
    '''
    if len(deck) != 0:
        current_card = deck.pop(0)
        while current_card[1] < 5 or current_card[1] > 10:
            opponent_hand.append(current_card)
            if len(deck) == 0:
                break
            current_card = deck.pop(0)
        
        player_hand.append(current_card)
        
    player_hand.sort()
    
    # do cards + - 4 for second subset:
    if len(deck) != 0:
        current_card = deck.pop(0)
        # Add this card to our hand if it is within 4 of the first card, remember Ace can be high or low:
        while current_card[1] >= player_hand[0][1] + 5 or current_card[1] <= player_hand[0][1] - 5:
            
            if current_card[1] == 14 and player_hand[0][1] <= 5:
                break
            else:
                opponent_hand.append(current_card)
            
            if len(deck) == 0:
                break
            current_card = deck.pop(0)
            
        if len(deck) != 0:
            player_hand.append(current_card)
            
    #Sort for order
    player_hand.sort()
    
    # Take all cards less than 5 ranks higher than min card, and less than 5 ranks lower than max card:
    
    if len(deck) != 0:
        current_card = deck.pop(0)
        while current_card[1] >= player_hand[0][1] + 5 or current_card[1] <= player_hand[4][1] - 5:
            
            if current_card[1] == 14 and player_hand[4][1] >= 10:
                break
            else:
                opponent_hand.append(current_card)
            
            if len(deck) == 0:
                break
            current_card = deck.pop(0)
        
        if len(deck) != 0:
            player_hand.append(current_card)

    player_hand.sort()
    '''
    
    #9 house implementation:
    

    # Step 1: Take any two cards with rank 9 or above
    while len(player_hand) < 2 and deck:
        card = deck.pop(0)
        if card[1] >= 9:
            player_hand.append(card)
        else:
            opponent_hand.append(card)

    # Step 2: After picking two cards >=9, go for a full house using those values
    if len(player_hand) == 2:
        target_ranks = [card[1] for card in player_hand]
        while len(player_hand) < 5 and deck:
            card = deck.pop(0)
            if card[1] in target_ranks:
                player_hand.append(card)
            else:
                opponent_hand.append(card)
    
    
    
    
    



    '''


    #RF chase implementation:
    
    
    #First card is any card 10 or up
    if len(deck) != 0:
        current_card = deck.pop(0)
        while current_card[1] < 10:
            
            opponent_hand.append(current_card)
            if len(deck) == 0:
                break
            current_card = deck.pop(0)
            
        player_hand.append(current_card)
        
    player_hand.sort()
    
    #Second is any card same suit as first, +- 4
    if len(deck) != 0:
        current_card = deck.pop(0)
        while current_card[1] >= player_hand[0][1] + 5 or current_card[1] <= player_hand[0][1] - 5 or current_card[0] != player_hand[0][0]:
            
            opponent_hand.append(current_card)
            if len(deck) == 0:
                break
            current_card = deck.pop(0)
        
        player_hand.append(current_card)
    
    #Sort for order
    player_hand.sort()
    
    #diff = player_hand[1] - player_hand[0]
    
    #Third is any card same suit as first greater then big - 5 and less than small + diff
    if len(deck) != 0:
        current_card = deck.pop(0)
        while current_card[1] >= player_hand[0][1] + 5 or current_card[1] <= player_hand[1][1] - 5 or current_card[0] != player_hand[0][0]:
            
            opponent_hand.append(current_card)
            if len(deck) == 0:
                break
            current_card = deck.pop(0)
        
        player_hand.append(current_card)
    
    #Repeat 
    player_hand.sort()
    
    
    
    if len(deck) != 0:
        current_card = deck.pop(0)
        while current_card[1] >= player_hand[0][1] + 5 or current_card[1] <= player_hand[2][1] - 5 or current_card[0] != player_hand[0][0]:
            
            opponent_hand.append(current_card)
            if len(deck) == 0:
                break
            current_card = deck.pop(0)
        
        player_hand.append(current_card)
    
    
    player_hand.sort()
    
    
    
    if len(deck) != 0:

        current_card = deck.pop(0)
        while current_card[1] >= player_hand[0][1] + 5 or current_card[1] <= player_hand[3][1] - 5 or current_card[0] != player_hand[0][0]:
            
            opponent_hand.append(current_card)
            if len(deck) == 0:
                break
            current_card = deck.pop(0)
        
        player_hand.append(current_card)
    '''
    
    
    
    if len(deck) != 0:
        while len(opponent_hand) < 8: 
            opponent_hand.append(deck.pop(0))
        
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




