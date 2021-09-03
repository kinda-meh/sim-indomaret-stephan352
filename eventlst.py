import heapq


class EventList:
    def __init__(self, arrivals):
        heapq.heapify(arrivals)
        self.events = arrivals

    def get_events(self):
        return self.events

    def push(self, event):
        heapq.heappush(self.events, event)

    def pop(self):
        return heapq.heappop(self.events)
