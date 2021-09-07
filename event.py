class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other):
        if self.time == other.time:
            return isinstance(self, DoneEvent)
        return self.time < other.time

    def __repr__(self):
        return f"<Event || time: {self.time}, type: {type(self).__name__}>"


class ArrivalEvent(Event):
    pass


class DoneEvent(Event):
    def __init__(self, time, cashier):
        super().__init__(time)
        self.cashier = cashier
