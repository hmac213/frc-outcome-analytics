import requests
import string
import matplotlib.pyplot as plot
import itertools as iterate
from probability import calculate_match_probability
from alliance import alliance

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

class event:
    def __init__(self, event_code):
    
        self.event_code = event_code
        
        # get event data from API and convert from json
        self.get_event_matches = requests.get(f'https://www.thebluealliance.com/api/v3/event/{self.event_code}/matches', params = auth_TBA).json()
        self.get_alliances = requests.get(f'https://www.thebluealliance.com/api/v3/event/{self.event_code}/alliances', params = auth_TBA).json()
        
        self.alliances = []
        self.playoff_matches = []
        self.event_score = 0

        # initializing alliances and bracket type
        event_year = int(self.event_code[:4])
        for alliance_num in range(8):
            if event_year < 2023:
                self.alliances.append(alliance(event_code, alliance_num + 1, 'old'))
            else:
                self.alliances.append(alliance(event_code, alliance_num + 1, 'new'))

    def create_match_probability_distribution(self):
        # row is for alliance, col is against alliance
        probability_map = [[0] * 8 for i in range(8)]
        for i in range(8):
            for j in range(7 - i):
                probability_map[i][j + i + 1] = calculate_match_probability(self.alliances[i], self.alliances[i + j + 1])
                probability_map[j + i + 1][i] = 1 - probability_map[i][j + i + 1]

        print('probability map done')
        self.probability_map = probability_map
                
    def transition(self, state, substate, winning_index, current_state):
        distribution = self.probability_map

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
    
    def simulate_brackets(self):

        probabilities = {}

        playoff_matches = []
        for match in self.get_event_matches:
            if match['comp_level'] != 'qm' and match['actual_time'] != None:
                playoff_matches.append(match)

        rankings = [0 for _ in range(8)]
        r78 = []
        r56 = []

        # ok wait just use ['status']['double-elim-round'] to sort. its the easiest.
        for alliance in self.get_alliances:
            if alliance['status']['status'] == 'won':
                rankings[0] = int(alliance['name'][9])
            elif alliance['status']['double_elim_round'] == 'Finals':
                rankings[1] = int(alliance['name'][9])
            elif alliance['status']['double_elim_round'] == 'Round 5':
                rankings[2] = int(alliance['name'][9])
            elif alliance['status']['double_elim_round'] == 'Round 4':
                rankings[3] = int(alliance['name'][9])
            elif alliance['status']['double_elim_round'] == 'Round 3':
                r56.append(int(alliance['name'][9]))
            elif alliance['status']['double_elim_round'] == 'Round 2':
                r78.append(int(alliance['name'][9]))

        r56_scores = []

        for alliance in r56:
            r56_scores.append(self.alliances[alliance - 1].calculate_average_playoff_score())

        if r56_scores[0] > r56_scores[1]:
            rankings[4] = r56[0]
            rankings[5] = r56[1]
        else:
            rankings[4] = r56[1]
            rankings[5] = r56[0]

        r78_scores = []

        for alliance in r78:
            r78_scores.append(self.alliances[alliance - 1].calculate_average_playoff_score())

        if r78_scores[0] > r78_scores[1]:
            rankings[6] = r78[0]
            rankings[7] = r78[1]
        else:
            rankings[6] = r78[1]
            rankings[7] = r78[0]

        string_rankings = ''.join(str(rankings[i]) for i in range(8))

        print(string_rankings)

        for arrangement in iterate.product(range(2), repeat = 16):

            default_states = {
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
            counting_probability = counting_probability * self.transition('w1', 0, arrangement[0], states)
            counting_probability = counting_probability * self.transition('w1', 1, arrangement[1], states)
            counting_probability = counting_probability * self.transition('w1', 2, arrangement[2], states)
            counting_probability = counting_probability * self.transition('w1', 3, arrangement[3], states)
            counting_probability = counting_probability * self.transition('w2', 0, arrangement[4], states)
            counting_probability = counting_probability * self.transition('w2', 1, arrangement[5], states)
            counting_probability = counting_probability * self.transition('w3', 0, arrangement[6], states)
            counting_probability = counting_probability * self.transition('l1', 0, arrangement[7], states)
            counting_probability = counting_probability * self.transition('l1', 1, arrangement[8], states)
            counting_probability = counting_probability * self.transition('l2', 0, arrangement[9], states)
            counting_probability = counting_probability * self.transition('l2', 1, arrangement[10], states)
            counting_probability = counting_probability * self.transition('l3', 0, arrangement[11], states)
            counting_probability = counting_probability * self.transition('l4', 0, arrangement[12], states)
            counting_probability = counting_probability * self.transition('f', 0, arrangement[13], states)
            counting_probability = counting_probability * self.transition('r56', 0, arrangement[14], states)
            counting_probability = counting_probability * self.transition('r78', 0, arrangement[15], states)

            final_order = str(states['r1'][0][0]) + str(states['r2'][0][0]) + str(states['r3'][0][0]) + str(states['r4'][0][0]) + str(states['r5'][0][0]) + str(states['r6'][0][0]) + str(states['r7'][0][0]) + str(states['r8'][0][0])

            if final_order in probabilities:
                probabilities[final_order] += counting_probability
            else:
                probabilities[final_order] = counting_probability

            states = default_states

        data_list = []
        for key in probabilities:
            data_list.append(probabilities[key])

        data_check = probabilities[string_rankings]
        cumulative_sum = 0

        for value in data_list:
            if value < data_check:
                cumulative_sum += value


        # plot.hist(data_list, bins = 3840)
        # plot.show()

        return cumulative_sum


        # get what actually happened and calculate the probability of it

        # the order is based on how we do the order above. actually we should move this to the top when we are done