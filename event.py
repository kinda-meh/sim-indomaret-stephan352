from enum import Enum


class Event:
    def __init__(self, time):
        self.time = time

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
    def __init__(self, time):
        super().__init__(time)
        self.type = EventType("arrive")

    @staticmethod
    def create(time):
        return ArrivalEvent(time)


class DoneEvent(Event):
    def __init__(self, time, cashier):
        super().__init__(time)
        self.type = EventType("done")
        self.cashier = cashier

    @staticmethod
    def create(time, cashier):
        return DoneEvent(time, cashier)
