from enum import Enum


class Event:
    def __init__(self, time, event_type):
        self.time = time
        self.type = event_type

    def __lt__(self, other):
        if self.time == other.time:
            return self.type == EventType.DONE
        return self.time < other.time

    def __repr__(self):
        return f"<Event || time: {self.time}, type: {self.type}>"


class EventType(Enum):
    ARRIVE = "arrive"
    DONE = "done"


class ArrivalEvent(Event):
    @staticmethod
    def create(time, event_type):
        return ArrivalEvent(time, event_type)

class DoneEvent(Event):
    def __init__(self, time, event_type, cashier):
        super().__init__(time, event_type)
        self.cashier = cashier

    @staticmethod
    def create(time, event_type, cashier):
        return DoneEvent(time, event_type, cashier)
