from event import event
import statbotics

sb = statbotics.Statbotics()

event_list = sb.get_events(2024, fields = ['key'])

event_cumulative_outcomes = {}

for key in event_list:
    this_event = event(key['key'])
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


