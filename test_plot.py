import matplotlib.pyplot as plot
from event import event
import itertools as iteration

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

distribution = [[0, 0.547, 0.974, 0.99, 0.981, 1.0, 0.992, 0.994], [0.45299999999999996, 0, 0.964, 0.971, 0.975, 1.0, 0.988, 0.99], [0.026000000000000023, 0.03600000000000003, 0, 0.569, 0.632, 0.891, 0.779, 0.848], [0.010000000000000009, 0.029000000000000026, 0.43100000000000005, 0, 0.54, 0.852, 0.681, 0.808], [0.019000000000000017, 0.025000000000000022, 0.368, 0.45999999999999996, 0, 0.808, 0.66, 0.72], [0.0, 0.0, 0.10899999999999999, 0.14800000000000002, 0.19199999999999995, 0, 0.298, 0.442], [0.008000000000000007, 0.01200000000000001, 0.22099999999999997, 0.31899999999999995, 0.33999999999999997, 0.702, 0, 0.631], [0.006000000000000005, 0.010000000000000009, 0.15200000000000002, 0.19199999999999995, 0.28, 0.558, 0.369, 0]]

# Code to simulate bracket

probabilities = []
teams = [1, 2, 3, 4, 5, 6, 7, 8]

states = {
    'w1' : [[1, 8], [4, 5], [2, 7], [3, 6]],
    'w2' : [[0, 0], [0, 0]],
    'w3' : [[0, 0]],
    'l1' : [[0, 0], [0,0]],
    'l2' : [[0, 0], [0,0]],
    'l3' : [[0, 0]],
    'l4' : [[0, 0]],
    'f' : [[0,0]],
    'r1' : 0,
    'r2' : 0,
    'r3' : 0,
    'r4' : 0,
    'r5' : 0,
    'r6' : 0,
    'r7' : 0,
    'r8' : 0
}

# create variables to hold the rank ties. Will deal with them seperately

seven_eight_tie = [0, 0]
five_six_tie = [0, 0]

transition_map = {
    'w1' : ['w2', 'l1'],
    'w2' : ['w3', 'l2'],
    'w3' : ['w4', 'l4'],
    'l1' : ['l2', seven_eight_tie],
    'l2' : ['l3', five_six_tie],
    'l3' : ['l4', 'r4'],
    'l4' : ['f', 'r3'],
    'f' : ['r1', 'r2']
}

# the 'state' parameter must be of the form states[state][substate], to create universal syntax
def transition(state, winning_color, substate):
    if winning_color == 'red':
        states[transition_map[state][0]] = states[state][substate][0]
        states[transition_map[state][1]] = states[state][substate][1]
    elif winning_color == 'blue':
        states[transition_map[state][0]] = states[state][substate][1]
        states[transition_map[state][1]] = states[state][substate][0]

def check_order():
    order = [states['r1'], states['r2'], states['r3'], states['r4'], states['r5'], states['r6'], states['r7'], states['r8']]

    


print(len(probabilities))