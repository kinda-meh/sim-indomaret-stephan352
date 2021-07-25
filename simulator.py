from event import Event, EventType


class Simulator:
    def __init__(self, arrivals, service_time=2.0):
        self.events = arrivals
        self.service_time = service_time
        self.last_dispatched_id = 0
        self.customers = []

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

    def _serve_cust(self, time, cust_id):
        assert self.customer_served is None
        assert self.customer_waiting is None

        print(f'{time:5.3f} {cust_id:03} served')
        self.num_served_customers += 1
        self.customer_served = cust_id
        self._push(Event(time + self.service_time, EventType.DONE))

        assert self.customer_served is not None
        assert self.customer_waiting is None

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

    def _on_arrive(self, time, cust_id):
        print(f'{time:5.3f} {cust_id:03} arrives')
        current_customer = tuple(filter(lambda cust: cust.cust_id == cust_id, self.customers))[0]
        current_customer.do_initial_actions()

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
                new_customer = customer(event.time, self.last_dispatched_id, self)
                self.customers += [new_customer,]
                self._on_arrive(event.time, new_customer.cust_id)
            else:
                self._on_done(event.time)
        served = self.num_served_customers
        lost = self.num_lost_customers
        ave_waiting_time = self.total_waiting_time / served
        return ave_waiting_time, served, lost

class customer:
    def __init__(self, time_arrived, cust_id, in_simulator):
        self.time_arrtived = time_arrived
        self.cust_id = cust_id
        self.simulator = in_simulator

    def do_initial_actions(self):
        if self.simulator.customer_served is None:
            self.simulator._serve_cust(self.time_arrtived, self.cust_id)
        elif self.simulator.customer_waiting is None:
            self.wait()
        else:
            self.leave()

    def leave(self):
        assert self.simulator.customer_served is not None
        assert self.simulator.customer_waiting is not None
        self.simulator.num_lost_customers += 1
        print(f'{self.time_arrtived:5.3f} {self.cust_id:03} leaves')

    def wait(self):
        assert self.simulator.customer_served is not None
        assert self.simulator.customer_waiting is None

        print(f'{self.time_arrtived:5.3f} {self.cust_id:03} waiting')
        self.simulator.start_waiting_time = self.time_arrtived
        self.simulator.customer_waiting = self.cust_id

        assert self.simulator.customer_served is not None
        assert self.simulator.customer_waiting is not None

# cust_id needs to stop being an argument