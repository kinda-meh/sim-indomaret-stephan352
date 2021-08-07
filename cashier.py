from customer import Customer


class Cashier:
    def __init__(self,service_time=2.0):
        self.service_time = service_time

        self.customer_serving = None
        self.customer_waiting = None

        self.customers_met = []
        self.total_waiting_time = 0
        self.num_served_customers = 0
        self.num_lost_customers = 0

    def serve_cust(self, time, customer):
        assert self.customer_serving is None
        assert self.customer_waiting is None

        print(f'{time:5.3f} {customer.id:03} served')
        self.num_served_customers += 1
        self.customer_serving = customer

        assert self.customer_serving is not None
        assert self.customer_waiting is None

    def make_cust_wait(self, time, customer):
        assert self.customer_serving is not None
        assert self.customer_waiting is None

        customer.wait(time)
        self.customer_waiting = customer

        assert self.customer_serving is not None
        assert self.customer_waiting is not None

    def refuse_customer(self, customer):
        assert self.customer_serving is not None
        assert self.customer_waiting is not None
        customer.leave()
        self.num_lost_customers += 1

    def on_cust_arrive(self, time, customer):
        print(f'customer {customer.id} checks cashier')
        print('===========================')
        if self.customer_serving:
            print('serving:', self.customer_serving.id)
        else:
            print('serving:', self.customer_serving)
        if self.customer_waiting:
            print('waiting:', self.customer_waiting.id)
        else:
            print('waiting:', self.customer_waiting)
        print('===========================')
        if self.customer_serving is None:
            print(f'cashier serving cust {customer.id}')
            self.serve_cust(time, customer)
        elif self.customer_waiting is None:
            print(f'cashier makes cust {customer.id} wait')
            self.make_cust_wait(time, customer)
        else:
            print(f'cashier refuses cust {customer.id}')
            self.refuse_customer(customer)

    def on_done(self, time):
        assert self.customer_serving is not None
        print(f'{time:5.3f} {self.customer_serving.id:03} done')
        self.customer_serving = None
        if self.customer_waiting is not None:
            self.serve_waiting(time)

    def serve_waiting(self, time):
        assert self.customer_serving is None
        assert self.customer_waiting is not None

        customer, self.customer_waiting = self.customer_waiting, None
        self.total_waiting_time += time - customer.arrival_time
        print(f'{time:5.3f} {customer.id:03} done waiting')
        self.serve_cust(time, customer)

        assert self.customer_serving is not None
        assert self.customer_waiting is None



