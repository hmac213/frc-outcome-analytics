import matplotlib.pyplot as plot
from event import event
import itertools as iterate
from decimal import Decimal, getcontext

getcontext().prec = 50

# Paths to 8 seed:
# W1 -> L1 -> 8
# Paths to 7 seed:
# W1 -> L1 -> 7 via higher average score
# Paths to 6 seed:
# W1 -> W2 -> L2
# W1 -> L1 -> L2
# Paths to 5 seed:
# W1 -> W2 -> L2 via higher average score
# W1 -> L1 -> L2 via higher average score
# Paths to 4 seed:
# W1 -> W2 -> L2 -> L3
# W1 -> L1 -> L2 -> L3
# Paths to 3 seed:
# W1 -> W2 -> W3 -> L4
# W1 -> W2 -> L2 -> L3 -> L4
# W1 -> L1 -> L2 -> L3 -> L4
# Path to 2 seed:
# W1 -> W2 -> W3 -> F
# W1 -> W2 -> W3 -> L4 -> F
# W1 -> W2 -> L2 -> L3 -> L4 -> F
# W1 -> L1 -> L2 -> L3 -> L4 -> F
# Path to 1 seed:
# W1 -> W2 -> W3 -> F win
# W1 -> W2 -> W3 -> L4 -> F win
# W1 -> W2 -> L2 -> L3 -> L4 -> F win
# W1 -> L1 -> L2 -> L3 -> L4 -> F win

distribution = [[0, 0.547, 0.974, 0.99, 0.981, 0.997, 0.992, 0.994], [0.45299999999999996, 0, 0.964, 0.971, 0.975, 0.996, 0.988, 0.99], [0.026000000000000023, 0.03600000000000003, 0, 0.569, 0.632, 0.891, 0.779, 0.848], [0.010000000000000009, 0.029000000000000026, 0.43100000000000005, 0, 0.54, 0.852, 0.681, 0.808], [0.019000000000000017, 0.025000000000000022, 0.368, 0.45999999999999996, 0, 0.808, 0.66, 0.72], [0.003, 0.004, 0.10899999999999999, 0.14800000000000002, 0.19199999999999995, 0, 0.298, 0.442], [0.008000000000000007, 0.01200000000000001, 0.22099999999999997, 0.31899999999999995, 0.33999999999999997, 0.702, 0, 0.631], [0.006000000000000005, 0.010000000000000009, 0.15200000000000002, 0.19199999999999995, 0.28, 0.558, 0.369, 0]]

# Code to simulate bracket

default_states = {
    'w1' : [[1, 8], [3, 5], [2, 7], [3, 6]],
    'w2' : [[], []],
    'w3' : [[]],
    'l1' : [[], []],
    'l2' : [[], []],
    'l3' : [[]],
    'l4' : [[]],
    'f' : [[]],
    'r1' : [[]],
    'r2' : [[]],
    'r3' : [[]],
    'r4' : [[]],
    'r5' : [[]],
    'r6' : [[]],
    'r7' : [[]],
    'r8' : [[]],
    'r56' : [[]],
    'r78' : [[]]
}

# assigning paths to the alliances

path_one = [1, 8, 4, 5]
path_two = [2, 7, 3, 6]

transition_map = {
    'w1' : ['w2', 'l1'],
    'w2' : ['w3', 'l2'],
    'w3' : ['f', 'l4'],
    'l1' : ['l2', 'r78'],
    'l2' : ['l3', 'r56'],
    'l3' : ['l4', 'r4'],
    'l4' : ['f', 'r3'],
    'f' : ['r1', 'r2'],
    'r56' : ['r5', 'r6'],
    'r78' : ['r7', 'r8']
}

# the 'state' parameter must be of the form states[state][substate], to create universal syntax
# path is either 1 or 2. From path 1, you can access certain matches and from path 2 you can access certain matches
def transition(state, substate, winning_index, current_state):
    if state == 'w1':
        if substate == 0 or substate == 1:
            if winning_index == 0:
                current_state[transition_map[state][0]][0].append(current_state[state][substate][0])
                current_state[transition_map[state][1]][0].append(current_state[state][substate][1])
            elif winning_index == 1:
                current_state[transition_map[state][1]][0].append(current_state[state][substate][0])
                current_state[transition_map[state][0]][0].append(current_state[state][substate][1])
        elif substate == 2 or substate == 3:
            if winning_index == 0:
                current_state[transition_map[state][0]][1].append(current_state[state][substate][0])
                current_state[transition_map[state][1]][1].append(current_state[state][substate][1])
            elif winning_index == 1:
                current_state[transition_map[state][1]][1].append(current_state[state][substate][0])
                current_state[transition_map[state][0]][1].append(current_state[state][substate][1])
    elif state == 'l1':
        if winning_index == 0:
            current_state[transition_map[state][0]][substate].append(current_state[state][substate][0])
            current_state[transition_map[state][1]][0].append(current_state[state][substate][1])
        elif winning_index == 1:
            current_state[transition_map[state][1]][0].append(current_state[state][substate][0])
            current_state[transition_map[state][0]][substate].append(current_state[state][substate][1])
    elif state == 'w2':
        if substate == 0:
            substate_opp = 1
        elif substate == 1:
            substate_opp = 0
        if winning_index == 0:
            current_state[transition_map[state][0]][0].append(current_state[state][substate][0])
            current_state[transition_map[state][1]][substate_opp].append(current_state[state][substate][1])
        elif winning_index == 1:
            current_state[transition_map[state][1]][substate_opp].append(current_state[state][substate][0])
            current_state[transition_map[state][0]][0].append(current_state[state][substate][1])
    else:
        if winning_index == 0:
            current_state[transition_map[state][0]][0].append(current_state[state][substate][0])
            current_state[transition_map[state][1]][0].append(current_state[state][substate][1])
        elif winning_index == 1:
            current_state[transition_map[state][0]][0].append(current_state[state][substate][1])
            current_state[transition_map[state][1]][0].append(current_state[state][substate][0])

    for i in range(len(current_state[transition_map[state][0]])):
        if len(current_state[transition_map[state][0]][i]) == 2:
            current_state[transition_map[state][0]][i].sort()

    for i in range(len(current_state[transition_map[state][1]])):
        if len(current_state[transition_map[state][1]][i]) == 2:
            current_state[transition_map[state][1]][i].sort()

    if winning_index == 0:
        return distribution[current_state[state][substate][0] - 1][current_state[state][substate][1] - 1]
    else:
        return distribution[current_state[state][substate][1] - 1][current_state[state][substate][0] - 1]

# make sure the indices of these two following lists always align.

probabilities = {}

def simulate_brackets():
    # we sort based on indices.
    # simulating using binary
    # if number is 1, then red wins, if number is 0 then blue wins

    for arrangement in iterate.product(range(2), repeat = 16):

        states = {
            'w1' : [[1, 8], [4, 5], [2, 7], [3, 6]],
            'w2' : [[], []],
            'w3' : [[]],
            'l1' : [[], []],
            'l2' : [[], []],
            'l3' : [[]],
            'l4' : [[]],
            'f' : [[]],
            'r1' : [[]],
            'r2' : [[]],
            'r3' : [[]],
            'r4' : [[]],
            'r5' : [[]],
            'r6' : [[]],
            'r7' : [[]],
            'r8' : [[]],
            'r56' : [[]],
            'r78' : [[]]
        }

        counting_probability = 1
        counting_probability = counting_probability * transition('w1', 0, arrangement[0], states)
        counting_probability = counting_probability * transition('w1', 1, arrangement[1], states)
        counting_probability = counting_probability * transition('w1', 2, arrangement[2], states)
        counting_probability = counting_probability * transition('w1', 3, arrangement[3], states)
        counting_probability = counting_probability * transition('w2', 0, arrangement[4], states)
        counting_probability = counting_probability * transition('w2', 1, arrangement[5], states)
        counting_probability = counting_probability * transition('w3', 0, arrangement[6], states)
        counting_probability = counting_probability * transition('l1', 0, arrangement[7], states)
        counting_probability = counting_probability * transition('l1', 1, arrangement[8], states)
        counting_probability = counting_probability * transition('l2', 0, arrangement[9], states)
        counting_probability = counting_probability * transition('l2', 1, arrangement[10], states)
        counting_probability = counting_probability * transition('l3', 0, arrangement[11], states)
        counting_probability = counting_probability * transition('l4', 0, arrangement[12], states)
        counting_probability = counting_probability * transition('f', 0, arrangement[13], states)
        counting_probability = counting_probability * transition('r56', 0, arrangement[14], states)
        counting_probability = counting_probability * transition('r78', 0, arrangement[15], states)

        final_order = str(states['r1'][0][0]) + str(states['r2'][0][0]) + str(states['r3'][0][0]) + str(states['r4'][0][0]) + str(states['r5'][0][0]) + str(states['r6'][0][0]) + str(states['r7'][0][0]) + str(states['r8'][0][0])

        if final_order in probabilities:
            probabilities[final_order] += counting_probability
        else:
            probabilities[final_order] = counting_probability

        states = default_states

def create_plot():
    data_list = []
    for probability in probabilities:
        data_list.append(probabilities[probability])
    
    plot.hist(data_list, bins = 1920)
    plot.show()

simulate_brackets()
create_plot()


print(max(probabilities, key = probabilities.get))
print(probabilities['12453786'])