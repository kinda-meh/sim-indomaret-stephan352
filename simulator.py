from event import Event, EventType
from cashier import Cashier
from customer import Customer
from eventlst import EventList


class Simulator:
    def __init__(self, arrivals, no_of_cashiers=1):
        event_list = EventList(arrivals)
        self.events = event_list
        self.cashier = [Cashier(x, event_list) for x in range(1, no_of_cashiers + 1)]

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
        served = self.cashier[0].num_served_customers
        lost = self.cashier[0].num_lost_customers
        if self.cashier[0].total_waiting_time:
            ave_waiting_time = self.cashier[0].total_waiting_time / served
        else:
            ave_waiting_time = 0
        return ave_waiting_time, served, lost
