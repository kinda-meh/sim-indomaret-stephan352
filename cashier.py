from customer import Customer
from event import Event, EventType


class Cashier:
    def __init__(self, eq, service_time=2.0):
        self.service_time = service_time
        self.eq = eq
        self.id = None

        self.customer_serving = None
        self.customer_waiting = None

        self.total_waiting_time = 0
        self.num_served_customers = 0
        self.num_lost_customers = 0

    def serve_cust(self, time, customer):
        print(f"{time:5.3f} {customer.id:03} served")
        self.num_served_customers += 1
        self.customer_serving = customer
        self.eq.append(Event(time + self.service_time, EventType.DONE))



    def make_cust_wait(self, time, customer):
        customer.wait(time)
        self.customer_waiting = customer

    def refuse_customer(self, customer):
        customer.leave()
        self.num_lost_customers += 1

    def on_cust_arrive(self, time, customer):
        print(f"{time:5.3f} {customer.id:03} arrives")
        if self.customer_serving is None:
            self.serve_cust(time, customer)
        elif self.customer_waiting is None:
            self.make_cust_wait(time, customer)
        else:
            self.refuse_customer(customer)

    def on_done(self, time):
        print(f"{time:5.3f} {self.customer_serving.id:03} done")
        self.customer_serving = None
        if self.customer_waiting is not None:
            self.serve_waiting(time)

    def serve_waiting(self, time):
        customer, self.customer_waiting = self.customer_waiting, None
        self.total_waiting_time += time - customer.arrival_time
        print(f"{time:5.3f} {customer.id:03} done waiting")
        self.serve_cust(time, customer)
