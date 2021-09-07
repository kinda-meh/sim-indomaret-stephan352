from sys import argv
from simulator import Simulator


def main(inp):
    lst = list(inp)
    sim = Simulator(int(lst[0]), int(lst[1]), int(lst[2]), float(lst[3]), float(lst[4]))
    ave, served, lost = sim.run()
    ave = round(ave, 3)
    print(f"{ave} {served} {lost}")
    return ave, served, lost


if __name__ == "__main__":
    _, filename = argv
    with open(filename, "r") as f:
        main(f)
