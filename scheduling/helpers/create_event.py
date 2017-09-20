def create_recurring_events(base,recurringstr):
    sequence = Series(ruleString=recurringstr).save()
    base.series = sequence
    base.base = True
    duration = base.end - base.start#check that creates timedelta, WORKS
    derived = list(rrulestr(recurringstr, dtstart=event.base))
    for derivative in derived:
        Event(start=derivative,end=derivative+duration,series=sequence).save()
