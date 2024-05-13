import requests
import string
import matplotlib.pyplot as plot
import itertools
from probability import calculate_match_probability
from alliance import alliance

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

class event:
    def __init__(self, event_code):
    
        self.event_code = event_code
        
        # get event data from API and convert from json
        self.get_event_matches = requests.get(f'https://www.thebluealliance.com/api/v3/event/{self.event_code}/matches', params = auth_TBA).json()
        
        self.alliances = []
        self.playoff_matches = []
        self.event_score = 0

        # initializing alliances and bracket type
        for alliance_num in range(8):
            if int(self.event_code.strip(string.ascii_letters)) < 2023:
                self.alliances.append(alliance(event_code, alliance_num + 1, 'old'))
            else:
                self.alliances.append(alliance(event_code, alliance_num + 1, 'new'))
        
        # initializing matches for all alliances
        def init_matches(self):
            for match in self.get_event_matches:
                if match['comp_level'] != 'qm' and match['actual_time'] != None:
                    self.playoff_matches.append(match)
            for match in self.playoff_matches:
                for alliance in self.alliances:
                    if alliance.team1 in match['alliances']['red']['team_keys'] or alliance.team1 in match['alliances']['red']['surrogate_team_keys']:
                        alliance.init_match(match, 'red')
                    elif alliance.team1 in match['alliances']['blue']['team_keys'] or alliance.team1 in match['alliances']['blue']['surrogate_team_keys']:
                        alliance.init_match(match, 'blue')
            for alliance in self.alliances:
                    alliance.sort_matches()
            
        # init_matches(self)

    # define function to calculate final event rankings.
    def calculate_event_score(self):
        for alliance in self.alliances:
            self.event_score += abs(alliance.seed_num - alliance.final_ranking)

    # creating distribution of scores
    # need to make it so that the '0' distribution is more common, reflecting real life
    def draw_distribution(self):
        plot_data = []
        for arrangement in list(itertools.permutations(list(range(1,9)), 8)):
            arrangement_sum = 0
            for number in range(len(arrangement)):
                arrangement_sum += (1 / arrangement[number]) * abs(arrangement[number] - (number + 1))
            plot_data.append(arrangement_sum)
        plot.hist(plot_data, bins = 256)
        plot.show()

    def create_match_probability_distribution(self):
        # row is for alliance, col is against alliance
        probability_map = [[0] * 8 for i in range(8)]
        for i in range(8):
            for j in range(7 - i):
                probability_map[i][j + i + 1] = calculate_match_probability(self.alliances[i], self.alliances[i + j + 1])

        return probability_map
                
    def create_place_probability_distribution(self):
        initial_matches = 

cada = event('2024cada')
print(cada.create_probability_distribution())
        
        