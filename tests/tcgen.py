from sys import argv
from random import randint

def main():
    _, n = argv
    for i in range(int(n)):
        print(randint(0, 1000), "arrive")

if __name__ == "__main__":
    main()
