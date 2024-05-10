import statbotics
import requests
import string

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

sb = statbotics.Statbotics()

class alliance:
    def __init__(self, event_code, seed, bracket_style):
        get_alliances_json = requests.get(f'https://www.thebluealliance.com/api/v3/event/{event_code}/alliances', params = auth_TBA)
        get_alliances = get_alliances_json.json()
        self.event_code = event_code
        self.seed_num = seed
        self.seed_name = "Alliance " + str(seed)
        self.team1 = get_alliances[self.seed_num - 1]['picks'][0]
        self.team2 = get_alliances[self.seed_num - 1]['picks'][1]
        self.team3 = get_alliances[self.seed_num - 1]['picks'][2]
        if len(get_alliances[self.seed_num - 1]['picks']) == 4:
            self.team4 = get_alliances[self.seed_num - 1]['picks'][3]

        self.matches = []
        self.bracket_style = bracket_style

    def assign_match(self, matches):
        for match in matches:
            self.matches.append(match)