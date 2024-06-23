from event import event
import statbotics
import requests

sb = statbotics.Statbotics()

event_list = ['2023mxto', '2023nccmp', '2023dal']

values = []

for active_event in event_list:
    print('starting event: ' + active_event)
    this_event = event(active_event)
    this_event.create_match_probability_distribution()
    value = this_event.simulate_brackets()
    values.append(value)
    print(value)

print(values)

# 8 for 22

