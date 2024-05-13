from alliance import alliance
import statbotics
import scipy.stats as sp

sb = statbotics.Statbotics()

def calculate_win_prob (red_alliance: alliance, blue_alliance: alliance):
    # The win_prob variable calculates the probability of red winning. The probability of blue winning is 1 - win_prob

    # get expected match score

    red_average, red_standard_deviation, num_qual_matches = red_alliance.calculate_alliance_points_mean_sd()
    blue_average, blue_standard_deviation, num_qual_matches = blue_alliance.calculate_alliance_points_mean_sd()

    # conduct two-sample t-test to calculate probability of winning for red alliance

    # return sp.ttest_ind_from_stats(red_average, red_standard_deviation, num_qual_matches, blue_average, blue_standard_deviation, num_qual_matches, False, 'greater')

    return [red_average, red_standard_deviation, blue_average, blue_standard_deviation, sp.ttest_ind_from_stats(red_average, red_standard_deviation, num_qual_matches, blue_average, blue_standard_deviation, num_qual_matches, False, 'greater')]

print(calculate_win_prob(alliance('2024cada', 1, 'new'), alliance('2024cada', 2, 'new')))

