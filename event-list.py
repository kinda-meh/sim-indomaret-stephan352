class EventList:
    def __init__(self):
        self.events = list()

    def push(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events