from event import Event, EventType


class Cashier:
    def __init__(self, id, event_list, generator):
        self.generator = generator
        self.events = event_list
        self.id = id

        self.customer_serving = None
        self.customer_waiting = None

        self.total_waiting_time = 0
        self.num_served_customers = 0
        self.num_lost_customers = 0

    def get_cust_serving(self):
        return self.customer_serving

    def get_cust_waiting(self):
        return self.customer_waiting

    def push_to_list(self, event):
        self.events.push(event)

    def serve_cust(self, time, customer):
        print(f"{time:5.3f} C{customer.id} served by S{self.id}")
        self.num_served_customers += 1
        self.customer_serving = customer
        event = Event.create(float(time + self.generator.generate_service_time()), EventType("done"))
        event.note_cashier(self)
        self.push_to_list(event)

    def make_cust_wait(self, time, customer):
        customer.wait(time, self.id)
        self.customer_waiting = customer

    def on_done(self, time):
        print(f"{time:5.3f} C{self.customer_serving.id} done served by S{self.id}")
        self.customer_serving = None
        if self.customer_waiting is not None:
            self.serve_waiting(time)

    def serve_waiting(self, time):
        customer, self.customer_waiting = self.customer_waiting, None
        self.total_waiting_time += time - customer.arrival_time
        print(f"{time:5.3f} C{customer.id} done waiting for S{self.id}")
        self.serve_cust(time, customer)
