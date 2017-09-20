from scheduling import models
def get_events(window_start, window_end):
    return models.Event.objects.filter(start__gte=window_start).filter(end__lte=window_end)

def filter_events(sequence, window_start, window_end):#sequence is the list of events
    pass
