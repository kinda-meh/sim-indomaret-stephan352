# Selamat datang di Alfamart.

Alfamart memiliki **satu** *mba-mba* kasir, mereka hanya bisa menangani satu pelanggan dalam sekali waktu. Kali ini diasumsikan bahwa waktu yang dibutuhkan untuk menangani suatu pelanggan selalu sama yaitu `service_time`.

### SOP *mba-mba* Alfamart

- Saat pelanggan datang
  - Kalau tidak sedang menangani pelanggan, ia langsung menangani pelanggan.
  - Kalau ia sedang menangani pelanggan yang lain, pelanggan tersebut disuruh menunggu(mengantre).

### Perilaku pelanggan

Kalau ia melihat ada pelanggan yang sedang menunggu(mengantre) ia langsung gundah-gulana pulang dengan tangan kosong dan hati yang lesu.

### Observasi yang ingin kita lakukan

Diberikan list dari event kedatangan pelanggan, kita tertarik dengan 3 statistik.

- Rata-rata waktu tunggu pelanggan 
- Banyaknya pelanggan yang dilayani
- Banyaknya pelanggan yang pulang dengan tangan kosong dan hati yang lesu.

## Starter Code [procedural-imperative]

### Class `Event`

`Event` is written in a procedural manner. `Event` stores the `time` that it occurs and its `type`. 

```python
class Event:
    def __init__(self, time, event_type):
        self.time = time
        self.type = event_type

    @staticmethod
    def create(time, event_type):
      	""" Creates Event, don't change signature. """
        return Event(time, event_type)
```

### Enum `EventType`

We handle two types of events  `ARRIVE`  and `DONE`. `ARRIVE` means a customer arrival; while `DONE` means the customer is done being served.

```python
class EventType(Enum):
    ARRIVE = "arrive"
    DONE = "done"
```

### Class `Simulator`

`Simulator` is also written in procedural manner, it's quite an eyesore. Simulator is initiated with `arrivals` event list and `service_time`. 

```python
class Simulator:
    def __init__(self, arrivals, service_time=2.0):
      """ Initiates simulator, don't change signature. """
      self.events = arrivals
 				...
```

Basically `Simulator`, holds a list of upcoming events as `events`, and on `run`, it fetches the earliest event on `events` and act accordingly

```python
def run(self):
  	while self.events:
        event = self._pop() # get earliest event
        if event.type is EventType.ARRIVE:
            self.last_dispatched_id += 1
            cust_id = self.last_dispatched_id
            self._on_arrive(event.time, cust_id)
        else:
            self._on_done(event.time)
```

## How to run

`python main.py tests/tc-x.in` the solution is on `tests/tc-x.out`

## Task

Rewrite `Simulator` in OOP-manner. 

You can change anything except the signature of `Simulator.__init__`,  `Simulator::run`,  `Event.create` , `main`.

