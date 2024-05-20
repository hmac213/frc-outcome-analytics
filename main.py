from probability import calculate_match_probability
from event import event

test_event = event('2023arc')

test_event.create_match_probability_distribution()
test_event.simulate_brackets()

