from event import Event, EventType


class Cashier:
    def __init__(self, in_simulator, service_time):
        self.simulator = in_simulator
        self.service_time = service_time

    def serve_cust(self, time, customer):
        assert self.simulator.customer_served is None
        assert self.simulator.customer_waiting is None

        print(f'{time:5.3f} {customer.id:03} served')
        self.simulator.num_served_customers += 1
        self.simulator.customer_served = customer
        self.simulator._push(Event(time + self.service_time, EventType.DONE))

        assert self.simulator.customer_served is not None
        assert self.simulator.customer_waiting is None

    def serve_waiting(self, time):
        assert self.simulator.customer_served is None
        assert self.simulator.customer_waiting is not None

        cust, self.simulator.customer_waiting = self.simulator.customer_waiting, None
        self.simulator.total_waiting_time += time - self.simulator.start_waiting_time
        print(f'{time:5.3f} {cust.id:03} done waiting')
        self.serve_cust(time, cust)

        assert self.simulator.customer_served is not None
        assert self.simulator.customer_waiting is None

