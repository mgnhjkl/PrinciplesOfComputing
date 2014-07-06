"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(1)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = []
    sum_score = []
    contained = 0
    for dice in hand:
        contained = 0
        for index in range(len(scores)):
            if dice == scores[index][0]:
                scores[index][1] += dice
                contained = 1
                break
        if contained == 0:
            scores.append([dice, dice])
    for score_pair in scores:
        sum_score.append(score_pair[1])
    return max(sum_score)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [index + 1 for index in range(num_die_sides)]
    length = num_free_dice
    num_of_hands = 0
    scores = 0.0
    sequences = gen_all_sequences(outcomes, length)
    for sequence in sequences:
        hand = []
        for dice in held_dice:
            hand.append(dice)
        for index in range(num_free_dice):
            hand.append(sequence[index])
        scores += score(hand)
        num_of_hands += 1
    return scores / num_of_hands


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    used_dice = []
    holds = [()]
    last_layer_holds = [[[],-1]]
    for dummy_index in range(len(hand)):
        tmp_holds = last_layer_holds[:]
        last_layer_holds = []
        for hold in tmp_holds:
            used_dice = []
            for dice_index in range(hold[1] + 1, len(hand)):
                if hand[dice_index] not in used_dice:
                    tmp_hold = [[],0]
                    tmp_hold[0] = hold[0][:]
                    tmp_hold[1] = hold[1]
                    tmp_hold[0].append(hand[dice_index])
                    tmp_hold[1] = dice_index
                    used_dice.append(hand[dice_index])
                    last_layer_holds.append([tmp_hold[0], tmp_hold[1]])
                    holds.append(tuple(tmp_hold[0][:]))
    return set(holds)

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    holds = gen_all_holds(hand)
    max_value = 0.0
    max_value_hold = ()
    for hold in holds:
        value = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if value > max_value:
            max_value = value
            max_value_hold = hold
    return (max_value, max_value_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()
#print distinct_dices([1,1,3,3,3,5,5])
#print gen_all_holds((1,2,3,4,5))
#print [index + 1 for index in range(6)]
#print expected_value((2, 2), 6, 2)
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
print strategy((1,), 6)


    
    


