from sys import argv
from simulator import Simulator
from event import Event, EventType


def main():
    inputs = []
    _, filename = argv
    with open(filename, 'r') as f:
        inputs = [line for line in f]

    events = [Event.create(float(time), EventType(type_))
              for time, type_ in [line.split() for line in inputs]]

    sim = Simulator(events)
    ave, served, lost = sim.run()
    print(f'{ave:.6} {served} {lost}')


if __name__ == "__main__":
    main()
