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

# Need to create independent probabilities for calculating how likely a team is to get 8th place.

# P(T = 8) = P(Lose W1) * P(Lose L1) * P(Lose 7,8)
# P(T = 7) = P(Lose W1) * P(Lose L1) * P(Lose 7,8)
# P(T = 6) = [P(Win W1) * P(Lose W2) * P(Lose L2) + P(Lose W1) * P(Win L1) * P(Lose L2)] * P(Lose 5,6)

def create_distribution():
    # for loop to iterate through all
    for arrangement in list(iteration.permutations(list(range(1,9)), 8)):
        probability = 1
        # probability = 1
        # now we multiply by the certain events where 7 and 8 lose their first two matches and then the average score comparison
        # probability = probability * distribution[arrangement.get(0)][arrangement.get(7)] * distribution[arrangement.get(1)][arrangement.get(6)] * distribution[arrangement.get(6)][arrangement.get(7)]
        # now there are two possibilities for 5 and 6. Each can win then lose twice or lose win lose.
        # In the array below we use [5 win 6 win, 5 win 6 lose, 5 lose 6 win, 5 lose 6 lose]

        # In the first case, the probability that 5 and six both win their 
        # five_six_cp = [1, 1, 1, 1]
        # five_six_cp[0] = five_six_cp[0] * distribution[arrangement.get(4)][arrangement.get(3)] * distribution[arrangement.get(5)][arrangement.get(2)]

        for qf_arrangement in list(iteration.combinations(range(4,8), 2)):
            if arrangement[qf_arrangement[0]] + arrangement[qf_arrangement[1]] == 7:
                probability = 0
                break

        sf_exclusive_upper = [0, 7, 3, 4]
        sf_exclusive_lower = [1, 6, 2, 5]

        if (arrangement[2] in sf_exclusive_upper and arrangement[3] in sf_exclusive_upper) or (arrangement[2] in sf_exclusive_lower and arrangement[3] in sf_exclusive_lower):
            probability = 0

        if probability == 0:
            continue


        qf_winners = []
        sf_winners = []
        f_winners = []

        for i in range(4):
            if arrangement.get(i) < arrangement.get(7 - i):
                qf_winners.append(i)
            else:
                qf_winners.append(7 - i)

        probability = probability * distribution[arrangement.get(0)][arrangement.get(7)] * distribution[arrangement.get(1)][arrangement.get(6)] * distribution[arrangement.get(7)][arrangement.get(5)] * distribution[arrangement.get(3)][arrangement.get(4)]




        # 1, 8; 4, 5; 2, 7; 3, 6

create_distribution()
print(len(probabilities))