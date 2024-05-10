import statbotics
import requests
import string
from alliance import alliance

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

class event:
    def __init__(self, event_code):
        get_event_matches_json = requests.get(f'https://www.thebluealliance.com/api/v3/event/{event_code}/matches', params = auth_TBA)
        get_event_matches = get_event_matches_json.json()

        self.event_code = event_code

        self.alliances = []
        for alliance_num in range(8):
            if int(self.event_code.strip(string.ascii_letters)) < 2023:
                self.alliances.append(alliance(event_code, alliance_num, 'old'))
            else:
                self.alliances.append(alliance(event_code, alliance_num, 'new'))

        self.match_list = []
        def init_matches():
            for match in get_event_matches:
                if match['comp_level'] != 'qm':
                    self.match_list.append(match)
            for match in self.match_list:
                for alliance in self.alliances:
                    if alliance.team1 in match['alliances']['team_keys'] or alliance.team1 in match['alliances']['surrogate_team_keys']:
                        alliance.init_match(match)
        
        init_matches()


        
        