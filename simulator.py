from event import Event, EventType
from customer import Customer
from cashier import Cashier


class Simulator:
    def __init__(self, arrivals, service_time=2.0):
        self.events = arrivals
        self.last_dispatched_id = 0
        self.customers = []
        self.mba = Cashier(self, service_time)

        self.customer_served = None
        self.customer_waiting = None

        self.start_waiting_time = None
        self.total_waiting_time = 0
        self.num_served_customers = 0
        self.num_lost_customers = 0

    def _pop(self):
        event = min(self.events)
        self.events.remove(event)
        return event

    def _push(self, event):
        self.events.append(event)


    def _on_arrive(self, time, customer):
        print(f'{time:5.3f} {customer.id:03} arrives')
        current_customer = self.customers[-1]
        current_customer.do_initial_actions()


    def _on_done(self, time):
        assert self.customer_served is not None
        print(f'{time:5.3f} {self.customer_served.id:03} done')
        self.customer_served = None
        if self.customer_waiting is not None:
            self.mba.serve_waiting(time)

    def run(self):
        """ Returns triple of
                average waiting time,
                number of served customers,
                number of lost customers.
        """
        while self.events:
            event = self._pop()
            if event.type is EventType.ARRIVE:
                self.last_dispatched_id += 1
                new_customer = Customer(event.time, self.last_dispatched_id, self)
                self.customers.append(new_customer)
                self._on_arrive(event.time, new_customer)
            else:
                self._on_done(event.time)
        served = self.num_served_customers
        lost = self.num_lost_customers
        ave_waiting_time = self.total_waiting_time / served
        return ave_waiting_time, served, lost


