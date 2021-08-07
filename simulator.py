from event import Event, EventType
from cashier import Cashier
from customer import Customer


class Simulator:
    def __init__(self, arrivals, service_time=2.0):
        self.events = arrivals
        self.service_time = service_time
        self.last_dispatched_id = 0
        self.cashier = Cashier()

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

    def _cust_leaves(self, time, cust_id):
        assert self.customer_served is not None
        assert self.customer_waiting is not None
        self.num_lost_customers += 1
        print(f'{time:5.3f} {cust_id:03} leaves')

    def make_cashier_serve_cust(self, time, cashier, customer):
        cashier.serve_cust(time, customer)
        self._push(Event(time + cashier.service_time, EventType.DONE))

    def _serve_waiting(self, time):
        assert self.customer_served is None
        assert self.customer_waiting is not None

        cust, self.customer_waiting = self.customer_waiting, None
        self.total_waiting_time += time - self.start_waiting_time
        print(f'{time:5.3f} {cust:03} done waiting')
        self._serve_cust(time, cust)

        assert self.customer_served is not None
        assert self.customer_waiting is None

    def _make_cust_wait(self, time, cust_id):
        assert self.customer_served is not None
        assert self.customer_waiting is None

        print(f'{time:5.3f} {cust_id:03} waiting')
        self.start_waiting_time = time
        self.customer_waiting = cust_id

        assert self.customer_served is not None
        assert self.customer_waiting is not None

    def _on_arrive(self, time, cashier, customer):
        print(f'{time:5.3f} {customer.id:03} arrives')
        if cashier.customer_serving is None:
            cashier.serve_cust(time, customer)
            self._push(Event(time + self.service_time, EventType.DONE))
        elif cashier.customer_waiting is None:
            cashier.make_cust_wait(time, customer)
        else:
            cashier.refuse_customer(customer)

    def _on_done(self, time):
        assert self.customer_served is not None
        print(f'{time:5.3f} {self.customer_served:03} done')
        self.customer_served = None
        if self.customer_waiting is not None:
            self._serve_waiting(time)

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
                new_customer = Customer(event.time, self.last_dispatched_id)
                self._on_arrive(event.time, self.cashier, new_customer)
            else:
                self.cashier.on_done(event.time)
        served = self.cashier.num_served_customers
        lost = self.cashier.num_lost_customers
        ave_waiting_time = self.cashier.total_waiting_time / served
        return ave_waiting_time, served, lost