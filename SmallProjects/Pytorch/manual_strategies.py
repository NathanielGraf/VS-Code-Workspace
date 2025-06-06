from env import CardGameEnv

# Converts (suit, rank) to card index in [0, 51]
def card_to_index(suit, rank):
    suit_offset = {"H": 0, "D": 13, "C": 26, "S": 39}
    return suit_offset[suit] + (rank - 2)

# Strategy 1: Go for a Royal Flush in Hearts
def royal_flush_strategy(env):
    return [card_to_index("H", r) for r in [10, 11, 12, 13, 14]]

# Strategy 2: Take any 2 cards, then go for full house with their values
def full_house_with_start_strategy(env):
    if len(env.player_hand) < 2:
        # Just pick the top 2 cards in deck (not ideal but simple)
        return [card_to_index(*env.deck[0])]
    else:
        ranks = [c[1] for c in env.player_hand]
        target = set()
        for r in ranks:
            for s in "HDCS":
                target.add(card_to_index(s, r))
        return list(target)
    
def full_house_9plus_strategy(env):
    # Step 1: Pick any card with rank 9+
    if len(env.player_hand) < 2:
        # Filter for cards with rank 9+
        targets = [card_to_index(suit, rank)
                   for (suit, rank) in env.deck if rank >= 9]
        return targets
    
    else:
        # Step 2: Go for full house using first two card values
        ranks = [c[1] for c in env.player_hand]
        subset = set()
        for r in ranks:
            for s in "HDCS":
                subset.add(card_to_index(s, r))
        return list(subset)
    
def straight_strategy(env):
    hand_ranks = [c[1] for c in env.player_hand]


    # --- Step 1: If no cards yet, target any card with rank ∈ [5..10]
    if len(hand_ranks) == 0:
        return [card_to_index(s, r) for (s, r) in env.deck if 5 <= r <= 10]

    # --- Step 2: If exactly 1 card, target any card within ±4 of that rank (excluding same rank)
    if len(hand_ranks) == 1:
        single_rank = hand_ranks[0]
        targets = []
        for (s, r) in env.deck:
            if abs(single_rank - r) <= 4 and r != single_rank:
                targets.append(card_to_index(s, r))

        if single_rank == 5:
            targets.append(card_to_index("H", 14))
            targets.append(card_to_index("D", 14))
            targets.append(card_to_index("C", 14))
            targets.append(card_to_index("S", 14))

        return targets
    
    # If we have 2 cards, 
    if len(hand_ranks) == 2:
        hand_ranks.sort()
        card_difference = abs(hand_ranks[0] - hand_ranks[1])
        max_range = 4 - card_difference
        if hand_ranks[0] == 5 and hand_ranks[1] == 14:
            # Special case: if we have 5 and Ace, we can target any card with rank 2-
            return [card_to_index(s, r) for (s, r) in env.deck if 2 <= r <= 4]
            
        else: 
            return [card_to_index(s, r) for (s, r) in env.deck if hand_ranks[0] - max_range  <= r <= hand_ranks[1] + max_range and r not in hand_ranks]
            

    # If we have 3 cards, repeat the same logic as above, but with a larger range
    if len(hand_ranks) == 3:
        hand_ranks.sort()
        card_difference = abs(hand_ranks[0] - hand_ranks[-1])
        max_range = 4 - card_difference
        if 5 in hand_ranks and hand_ranks[-1] == 14:
            # Special case: if we have 5 and Ace, we can target any card with rank 2-
            return [card_to_index(s, r) for (s, r) in env.deck if 2 <= r <= 4 and r not in hand_ranks]

        else:
            return [card_to_index(s, r) for (s, r) in env.deck if hand_ranks[0] - max_range <= r <= hand_ranks[-1] + max_range and r not in hand_ranks]

    # If we have 4 cards, repeat the same logic as above, but with a larger range
    if len(hand_ranks) == 4:
        hand_ranks.sort()
        card_difference = abs(hand_ranks[0] - hand_ranks[-1])
        max_range = 4 - card_difference
        if 5 in hand_ranks and hand_ranks[-1] == 14:
            # Special case: if we have 5 and Ace, we can target any card with rank 2-
            return [card_to_index(s, r) for (s, r) in env.deck if 2 <= r <= 4 and r not in hand_ranks]

        else:
            return [card_to_index(s, r) for (s, r) in env.deck if hand_ranks[0] - max_range <= r <= hand_ranks[-1] + max_range and r not in hand_ranks]

    
    # --- If we already have 5 cards, return empty (no more targeting needed)
    return []

# Simulate episodes
def run_manual(env, strategy_fn, num_games):
    wins = 0
    for _ in range(num_games):
        env.reset()
        done = False
        while not done:
            subset = strategy_fn(env)
            obs, reward, done, _, win = env.step(subset)
        wins += int(win == 1)
    print(f"{strategy_fn.__name__} win rate: {wins / num_games:.2f}")

if __name__ == "__main__":
    env = CardGameEnv()
    run_manual(env, royal_flush_strategy, num_games=1000)
    run_manual(env, full_house_with_start_strategy, num_games=1000)
    run_manual(env, full_house_9plus_strategy, num_games=1000)
    run_manual(env, straight_strategy, num_games=1000)