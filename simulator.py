from event import Event, EventType
from cashier import Cashier
from customer import Customer


class Simulator:
    def __init__(self, arrivals, service_time=2.0):
        self.events = arrivals
        self.service_time = service_time
        self.cashier = Cashier(self.events, service_time)

    def _pop(self):
        event = min(self.events)
        self.events.remove(event)
        return event

    def run(self):
        """Returns triple of
        average waiting time,
        number of served customers,
        number of lost customers.
        """
        last_dispatched_id = 0
        while self.events:
            event = self._pop()
            if event.type is EventType.ARRIVE:
                last_dispatched_id += 1
                new_customer = Customer(event.time, last_dispatched_id)
                self.cashier.on_cust_arrive(event.time, new_customer)
            else:
                self.cashier.on_done(event.time)
        served = self.cashier.num_served_customers
        lost = self.cashier.num_lost_customers
        ave_waiting_time = self.cashier.total_waiting_time / served
        return ave_waiting_time, served, lost
