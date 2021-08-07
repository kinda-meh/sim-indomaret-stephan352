from event import Event, EventType
from cashier import Cashier
from customer import Customer


class Simulator:
    def __init__(self, arrivals, service_time=2.0):
        self.events = arrivals
        self.service_time = service_time
        self.last_dispatched_id = 0
        self.cashier = Cashier(self.events)
        self.num_served_customers = 0
        self.num_lost_customers = 0

    def _pop(self):
        event = min(self.events)
        self.events.remove(event)
        return event

    def _push(self, event):
        self.events.append(event)

    def _on_arrive(self, time, cashier, customer):
        print(f"{time:5.3f} {customer.id:03} arrives")
        if cashier.customer_serving is None:
            cashier.serve_cust(time, customer)
        elif cashier.customer_waiting is None:
            cashier.make_cust_wait(time, customer)
        else:
            cashier.refuse_customer(customer)

    def run(self):
        """Returns triple of
        average waiting time,
        number of served customers,
        number of lost customers.
        """
        while self.events:
            event = self._pop()
            if event.type is EventType.ARRIVE:
                self.last_dispatched_id += 1
                new_customer = Customer(event.time, self.last_dispatched_id)
                self._on_arrive(event.time, self.cashier, new_customer)
            else:
                self.cashier.on_done(event.time)
        served = self.cashier.num_served_customers
        lost = self.cashier.num_lost_customers
        ave_waiting_time = self.cashier.total_waiting_time / served
        return ave_waiting_time, served, lost
