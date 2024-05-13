from alliance import alliance
import statbotics
import scipy.stats as sp
import numpy as np

sb = statbotics.Statbotics()

def calculate_match_probability(red_alliance: alliance, blue_alliance: alliance):
    # return the first alliance's win probability

    # get expected match score and standard deviation

    red_average, red_standard_deviation, num_qual_matches = red_alliance.calculate_alliance_points_mean_sd()
    blue_average, blue_standard_deviation, num_qual_matches = blue_alliance.calculate_alliance_points_mean_sd()

    # simulate 1000 times and return the outcome of the simulation

    red_wins = 0
    blue_wins = 0

    for i in range(1000):
        red_score = red_average + red_standard_deviation * np.random.standard_t(9)
        blue_score = blue_average + blue_standard_deviation * np.random.standard_t(9)
        if red_score > blue_score:
            red_wins += 1
        else:
            blue_wins += 1


    return red_wins / (red_wins + blue_wins)

