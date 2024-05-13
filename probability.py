from alliance import alliance
import statbotics
import scipy.stats as sp
import numpy as np

sb = statbotics.Statbotics()

def calculate_win_prob (red_alliance: alliance, blue_alliance: alliance):
    # The win_prob variable calculates the probability of red winning. The probability of blue winning is 1 - win_prob

    # get expected match score

    red_average, red_standard_deviation, num_qual_matches = red_alliance.calculate_alliance_points_mean_sd()
    blue_average, blue_standard_deviation, num_qual_matches = blue_alliance.calculate_alliance_points_mean_sd()

    # conduct two-sample t-test to calculate probability of winning for red alliance

    # return sp.ttest_ind_from_stats(red_average, red_standard_deviation, num_qual_matches, blue_average, blue_standard_deviation, num_qual_matches, False, 'greater')

    red_wins = 0
    blue_wins = 0

    for i in range(1000):
        red_score = red_average + red_standard_deviation * np.random.standard_t(9)
        blue_score = blue_average + blue_standard_deviation * np.random.standard_t(9)
        if red_score > blue_score:
            red_wins += 1
        else:
            blue_wins += 1


    return [red_average, red_standard_deviation, blue_average, blue_standard_deviation, red_wins / (red_wins + blue_wins), red_wins, blue_wins]

print(calculate_win_prob(alliance('2024cabe', 1, 'new'), alliance('2024cabe', 2, 'new')))

