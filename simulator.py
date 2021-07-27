from event import Event, EventType


class Simulator:
    def __init__(self, arrivals, service_time=2.0):
        self.events = arrivals
        self.last_dispatched_id = 0
        self.customers = []
        self.mba = mba2(self, service_time)

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


    def _on_arrive(self, time, cust_id):
        print(f'{time:5.3f} {cust_id:03} arrives')
        current_customer = tuple(filter(lambda cust: cust.cust_id == cust_id, self.customers))[0]
        current_customer.do_initial_actions()

    def _on_done(self, time):
        assert self.customer_served is not None
        print(f'{time:5.3f} {self.customer_served:03} done')
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
        self.mba = in_simulator.mba

    def do_initial_actions(self):
        if self.simulator.customer_served is None:
            self.mba.serve_cust(self.time_arrtived, self.cust_id)
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

class mba2:
    def __init__(self, in_simulator, service_time):
        self.simulator = in_simulator
        self.service_time = service_time

    def serve_cust(self, time, cust_id):
        assert self.simulator.customer_served is None
        assert self.simulator.customer_waiting is None

        print(f'{time:5.3f} {cust_id:03} served')
        self.simulator.num_served_customers += 1
        self.simulator.customer_served = cust_id
        self.simulator._push(Event(time + self.service_time, EventType.DONE))

        assert self.simulator.customer_served is not None
        assert self.simulator.customer_waiting is None

    def serve_waiting(self, time):
        assert self.simulator.customer_served is None
        assert self.simulator.customer_waiting is not None

        cust, self.simulator.customer_waiting = self.simulator.customer_waiting, None
        self.simulator.total_waiting_time += time - self.simulator.start_waiting_time
        print(f'{time:5.3f} {cust:03} done waiting')
        self.serve_cust(time, cust)

        assert self.simulator.customer_served is not None
        assert self.simulator.customer_waiting is None