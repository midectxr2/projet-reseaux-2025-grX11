import sys
from network.Network import Network

if __name__ == "__main__":
    sim = Network(sys.argv[1])
    sim.run()