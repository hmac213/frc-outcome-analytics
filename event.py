import requests
import string
from alliance import alliance

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

class event:
    def __init__(self, event_code):
        # get event data from API and convert from json
        get_event_matches_json = requests.get(f'https://www.thebluealliance.com/api/v3/event/{event_code}/matches', params = auth_TBA)
        get_event_matches = get_event_matches_json.json()

        # initializing event characteristics
        self.event_code = event_code
        self.alliances = []
        self.match_list = []

        # initializing alliances and bracket type
        for alliance_num in range(8):
            if int(self.event_code.strip(string.ascii_letters)) < 2023:
                self.alliances.append(alliance(event_code, alliance_num + 1, 'old'))
            else:
                self.alliances.append(alliance(event_code, alliance_num + 1, 'new'))
        
        # initializing matches for all alliances
        def init_matches(self):
            for match in get_event_matches:
                if match['comp_level'] != 'qm' and match['actual_time'] != None:
                    self.match_list.append(match)
            for match in self.match_list:
                for alliance in self.alliances:
                    if alliance.team1 in match['alliances']['red']['team_keys'] or alliance.team1 in match['alliances']['red']['surrogate_team_keys']:
                        alliance.init_match(match, 'red')
                    elif alliance.team1 in match['alliances']['blue']['team_keys'] or alliance.team1 in match['alliances']['blue']['surrogate_team_keys']:
                        alliance.init_match(match, 'blue')
            for alliance in self.alliances:
                    alliance.sort_matches()
        
        init_matches(self)

        # define function to calculate final event rankings.
        self.rankings = [1, 2, 3, 4, 5, 6, 7, 8]
        def calculate_rankings(self):
            for alliance in self.alliances:
                for compare_alliance in self.alliances:
                    if alliance == compare_alliance:
                        continue



cada = event('2024cada')
        
        