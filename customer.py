class Customer:
    def __init__(self, arrival_time, cust_id):
        self.arrival_time = arrival_time
        self.id = cust_id

    def wait(self, time, id):
        print(f"{time:5.3f} C{self.id} waits for S{id}")

    def leave(self):
        print(f"{self.arrival_time:5.3f} C{self.id} leaves")
