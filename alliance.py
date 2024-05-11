import requests
import string

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

class alliance:
    def __init__(self, event_code, seed, bracket_style):
        # fetch alliance data from API and convert from json
        get_alliances_json = requests.get(f'https://www.thebluealliance.com/api/v3/event/{event_code}/alliances', params = auth_TBA)
        get_alliances = get_alliances_json.json()

        # initializing alliance characteristics
        self.event_code = event_code
        self.seed_num = seed
        self.bracket_style = bracket_style
        self.team1 = get_alliances[self.seed_num - 1]['picks'][0]
        self.team2 = get_alliances[self.seed_num - 1]['picks'][1]
        self.team3 = get_alliances[self.seed_num - 1]['picks'][2]
        self.matches = []
        self.match_colors = []
        
        # only include fourth team if it exists
        if len(get_alliances[self.seed_num - 1]['picks']) == 4:
            self.team4 = get_alliances[self.seed_num - 1]['picks'][3]

    def init_match(self, match, color):
        self.matches.append(match)
        self.match_colors.append(color)

    # sorting an alliance's matches in chronological order
    # LOOK INTO MATCH SORTING WITH 'match_number' INSTEAD
    def sort_matches(self):
        sorted_matches = []
        if self.bracket_style == 'old':
            for match in self.matches:
                if match['comp-level'] == 'qf':
                    sorted_matches.append(match)
                elif match['comp-level'] == 'sf':
                    sorted_matches.append(match)
                else:
                    sorted_matches.append(match)
        elif self.bracket_style == 'new':
            for match_index in range(len(self.matches)):
                for index in range(len(self.matches)):
                    if '_sf' + str(match_index + 1) + 'm' in self.matches[index]['key']:
                        sorted_matches.append(self.matches[match_index])
                    if '_f' in self.matches[index]['key'] and 'm' + str(match_index + 1) in self.matches[match_index]['key']:
                        sorted_matches.append(self.matches[match_index])
        
        self.matches = sorted_matches
        for match in self.matches:
            print('match sorted for alliance ' + str(self.seed_num) + ': ' + match['key'])