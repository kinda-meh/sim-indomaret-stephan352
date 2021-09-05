class Customer:
    def __init__(self, arrival_time, cust_id, service_time):
        self.arrival_time = arrival_time
        self.id = cust_id
        self.service_time = service_time

    def get_serve_time(self):
        return self.service_time

    def wait(self, time, id):
        print(f" {time:5.3f} C{self.id} waits for S{id} (Q: C{self.id})")

    def leave(self):
        print(f" {self.arrival_time:5.3f} C{self.id} leaves")
