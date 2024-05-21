from event import event
import statbotics
import requests

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

sb = statbotics.Statbotics()

event_list = requests.get(f'https://www.thebluealliance.com/api/v3/events/2024', params = auth_TBA).json()

event_cumulative_outcomes = {}

for entry in event_list:
    if entry['division_keys'] != [] or entry['event_type_string'] == 'Offseason' or entry['event_type_string'] == 'Preseason':
        continue
    if entry['event_code'] == 'flwp':
        continue
    this_event = event(str(entry['year']) + entry['event_code'])
    print(f'starting event: {str(entry['year']) + entry['event_code']}')
    this_event.create_match_probability_distribution()
    event_cumulative_outcomes[this_event] = this_event.simulate_brackets()

num_upset_events = 0
num_typical_events = 0
for key in event_cumulative_outcomes:
    if event_cumulative_outcomes[key] < .5:
        num_upset_events += 1
    else:
        num_typical_events += 1

print(num_upset_events, num_typical_events)

# test_event = event('2024flwp')
# test_event.create_match_probability_distribution()
# print(test_event.simulate_brackets())


