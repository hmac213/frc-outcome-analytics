from event import event
import statbotics
import requests

auth_TBA = {'X-TBA-Auth-Key' : '319O7fm4AYptga0ktUY6oIW4uLfUqatprLsxyyFkymObLkYbo7u4lSi8jJ9UJT3f'}

sb = statbotics.Statbotics()

event_list = requests.get(f'https://www.thebluealliance.com/api/v3/events/2024', params = auth_TBA).json()

regional_events = []
district_events = []
district_championships = []
championship_divisions = []
events = []

for event_item in event_list:
    if event_item['division_keys'] == []:
        if event_item['event_type_string'] == 'Regional':
            regional_events.append(event_item['event_code'])
            events.append(event_item['event_code'])
        if event_item['event_type_string'] == 'District':
            district_events.append(event_item['event_code'])
            events.append(event_item['event_code'])
        if event_item['event_type_string'] == 'District Championship':
            district_championships.append(event_item['event_code'])
            events.append(event_item['event_code'])
        if event_item['event_type_string'] == 'Championship Division':
            championship_divisions.append(event_item['event_code'])
            events.append(event_item['event_code'])

event_num = len(regional_events) + len(district_events) + len(district_championships) + len(championship_divisions)

print(event_num)
print(regional_events)
print(district_events)
print(district_championships)
print(championship_divisions)
print(events[29])
print(events[30])
print(events[31])