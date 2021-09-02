from event import EventType, Event
from cashier import Cashier
from customer import Customer
from eventlst import EventList
from rng import RandomGenerator


class Simulator:
    def __init__(self, seed, no_of_cashiers, no_of_customers, arrival_constant, service_constant):
        generator = RandomGenerator(seed, arrival_constant, service_constant)

        service_time = generator.generate_service_time()


        event_list = EventList(self.make_events(generator, no_of_customers))
        self.events = event_list
        self.cashier = [Cashier(x, event_list, service_time) for x in range(1, no_of_cashiers + 1)]


        self.no_lost_customers = 0

    def make_events(self, generator, no_of_customers):
        arrivals = []
        T = 0
        for i in range(no_of_customers):
            arrivals.append(Event.create(float(T), EventType("arrive")))
            T += generator.generate_inter_arrival_time()
        return arrivals

    def find_first_idle_cash(self):
        for cash in self.cashier:
            if not cash.get_cust_serving():
                return cash
        return None

    def find_first_no_wait(self):
        for cash in self.cashier:
            if not cash.get_cust_waiting():
                return cash
        return None

    def direct_cust_to_cash(self, time, customer):
        print(f"{time:5.3f} {customer.id:03} arrives")
        idle_cash = self.find_first_idle_cash()
        if idle_cash:
            idle_cash.serve_cust(time, customer)
            return None
        nowait_cash = self.find_first_no_wait()
        if nowait_cash:
            nowait_cash.make_cust_wait(time, customer)
        else:
            customer.leave()
            self.no_lost_customers += 1

    def run(self):
        last_dispatched_id = 0
        while self.events.is_events_still_there():
            event = self.events.pop()
            if event.type is EventType.ARRIVE:
                last_dispatched_id += 1
                new_customer = Customer(event.time, last_dispatched_id)
                self.direct_cust_to_cash(event.time, new_customer)
            else:
                event.cashier.on_done(event.time)
        served_list = tuple(map(lambda x: x.num_served_customers, self.cashier))
        served = sum(served_list)
        waiting_times = tuple(map(lambda x: x.total_waiting_time, self.cashier))
        total_wait_time = sum(waiting_times)
        lost = self.no_lost_customers
        try:
            ave_waiting_time = total_wait_time / served
        except ZeroDivisionError:
            ave_waiting_time = 0
        return ave_waiting_time, served, lost
