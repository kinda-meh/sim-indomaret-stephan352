from sys import argv
from simulator import Simulator
from event import Event, EventType


def main(inp):
    lst = list(inp)
    print(lst)
    seed = int(lst[0])
    no_of_cashiers = int(lst[1])
    no_of_customers = int(lst[2])
    arrival_constant = float(lst[3])
    service_constant = float(lst[4])

    sim = Simulator(seed, no_of_cashiers, no_of_customers, arrival_constant, service_constant)
    ave, served, lost = sim.run()
    print(f"{float(ave):.3} {served} {lost}")
    return ave, served, lost


if __name__ == "__main__":
    _, filename = argv
    with open(filename, "r") as f:
        main(f)
