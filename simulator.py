from event import Event, EventType
from cashier import Cashier
from customer import Customer
from eventlst import EventList


class Simulator:
    def __init__(self, arrivals):
        event_list = EventList(arrivals)
        self.events = event_list
        self.cashier = Cashier(event_list)

    def _pop(self):
        return self.events.pop()

    def run(self):
        last_dispatched_id = 0
        while self.events.is_events_still_there():
            event = self._pop()
            if event.type is EventType.ARRIVE:
                last_dispatched_id += 1
                new_customer = Customer(event.time, last_dispatched_id)
                self.cashier.on_cust_arrive(event.time, new_customer)
            else:
                self.cashier.on_done(event.time)
        served = self.cashier.num_served_customers
        lost = self.cashier.num_lost_customers
        if self.cashier.total_waiting_time:
            ave_waiting_time = self.cashier.total_waiting_time / served
        else:
            ave_waiting_time = 0
        return ave_waiting_time, served, lost
