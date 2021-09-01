import heapq


class EventList:
    def __init__(self, arrivals):
        heapq.heapify(arrivals)
        self.events = arrivals

    def is_events_still_there(self):
        return self.events

    def push(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events

    def pop(self):
        return heapq.heappop(self.events)

