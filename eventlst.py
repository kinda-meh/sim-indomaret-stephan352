class EventList:
    def __init__(self, arrivals):
        self.events = arrivals

    def is_events_still_there(self):
        return self.events

    def push(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events

    def pop(self):
        event = min(self.events)
        self.events.remove(event)
        return event
