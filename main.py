from sys import argv
from simulator import Simulator
from event import Event, EventType


def main(inp):
    lst = list(inp)
    no_of_cashiers = int(lst[0])
    events = [Event.create(float(time), EventType("arrive")) for time in lst[1:]]

    sim = Simulator(events, no_of_cashiers)
    ave, served, lost = sim.run()
    print(f"{float(ave):.2} {served} {lost}")
    return ave, served, lost


if __name__ == "__main__":
    _, filename = argv
    with open(filename, "r") as f:
        main(f)
