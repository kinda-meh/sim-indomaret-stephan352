from event import Event, EventType


class Cashier:
    def __init__(self, id, event_list):
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
        if self.customer_waiting:
            print(f"{time:5.3f} C{customer.id} served by S{self.id} (Q: C{self.customer_waiting.id})")
        else:
            print(f"{time:5.3f} C{customer.id} served by S{self.id} (Q: null)")
        self.num_served_customers += 1
        self.customer_serving = customer
        event = Event.create(float(time + customer.get_serve_time()), EventType("done"))
        event.note_cashier(self)
        self.push_to_list(event)

    def make_cust_wait(self, time, customer):
        customer.wait(time, self.id)
        self.customer_waiting = customer

    def on_done(self, time):
        if self.customer_waiting:
            print(f"{time:5.3f} C{self.customer_serving.id} done served by S{self.id} (Q: C{self.customer_waiting.id})")
        else:
            print(f"{time:5.3f} C{self.customer_serving.id} done served by S{self.id} (Q: null)")
        self.customer_serving = None
        if self.customer_waiting is not None:
            self.serve_waiting(time)

    def serve_waiting(self, time):
        customer, self.customer_waiting = self.customer_waiting, None
        self.total_waiting_time += time - customer.arrival_time
        self.serve_cust(time, customer)
