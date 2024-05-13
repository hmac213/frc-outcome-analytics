import requests
import statbotics
import string
import math

sb = statbotics.Statbotics()

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

class alliance:
    def __init__(self, event_code, seed, bracket_style):

        self.event_code = event_code

        # fetch alliance data from API and convert from json
        self.get_alliances = requests.get(f'https://www.thebluealliance.com/api/v3/event/{self.event_code}/alliances', params = auth_TBA).json()
        self.get_event_matches = requests.get(f'https://www.thebluealliance.com/api/v3/event/{self.event_code}/matches', params = auth_TBA).json()

        self.seed_num = seed
        self.bracket_style = bracket_style
        self.init_teams()
        self.matches = []
        self.match_colors = []

    # initialize teams to the alliance
    def init_teams(self):
        self.teams = []
        for i in range(3):
            self.teams.append(int(self.get_alliances[self.seed_num - 1]['picks'][i].strip(string.ascii_letters)))
        if len(self.get_alliances[self.seed_num - 1]['picks']) == 4:
            self.teams.append(int(self.get_alliances[self.seed_num - 1]['picks'][3].strip(string.ascii_letters)))

    def calculate_alliance_points_mean_sd(self):
        alliance_points_mean = 0
        alliance_variance = 0
        num_qual_matches = sb.get_team_event(self.teams[0], event = self.event_code, fields = ['qual_count'])['qual_count']

        for pick_num in range(3):
            alliance_points_mean += sb.get_team_event(self.teams[pick_num], event = self.event_code, fields = ['epa_pre_playoffs'])['epa_pre_playoffs']
        
        for i in range(3):
            team_average_qual_score = 0
            qual_match_scores = []
            # should speed up code by not calling API for every team. Should rather create a match list beforehand and assign to teams based on being in the match.
            qual_matches = requests.get(f'https://www.thebluealliance.com/api/v3/team/frc{self.teams[i]}/event/{self.event_code}/matches/simple', params = auth_TBA).json()
            
            updated_qual_matches = []
            for match in qual_matches:
                if match['comp_level'] == 'qm':
                    updated_qual_matches.append(match)

            qual_matches = updated_qual_matches

            for match in qual_matches:
                if 'frc' + str(self.teams[i]) in match['alliances']['red']['team_keys']:
                    team_average_qual_score += (match['alliances']['red']['score'] / num_qual_matches)
                    qual_match_scores.append(match['alliances']['red']['score'])
                else:
                    team_average_qual_score += (match['alliances']['blue']['score'] / num_qual_matches)
                    qual_match_scores.append(match['alliances']['blue']['score'])

            percent_contribution = sb.get_team_event(self.teams[i], event = self.event_code, fields = ['epa_pre_playoffs'])['epa_pre_playoffs'] / team_average_qual_score

            team_variance = 0

            for j in range(num_qual_matches):
                team_variance += (pow(qual_match_scores[j] - team_average_qual_score, 2) * pow(percent_contribution, 2))

            team_variance = team_variance / (num_qual_matches - 1)

            alliance_variance += team_variance

        alliance_sd = math.sqrt(alliance_variance)

        return [alliance_points_mean, alliance_sd, num_qual_matches]

    def init_match(self, match, color):
        self.matches.append(match)
        self.match_colors.append(color)

    # sorting an alliance's matches in chronological order
    # Need to redo all of this
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