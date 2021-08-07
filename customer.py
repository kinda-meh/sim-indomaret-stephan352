class Customer:
    def __init__(self, arrival_time, cust_id):
        self.arrival_time = arrival_time
        self.id = cust_id

    def wait(self, time):
        print(f'{time:5.3f} {self.id:03} waiting')

    def leave(self):
        print(f'{self.arrival_time:5.3f} {self.id:03} leaves')