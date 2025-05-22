import json
from src.network.Packet import *
from src.network.Link import *

class Router:
    def __init__(self, router_id, simulator):
        self.id = router_id
        self.simulator = simulator
        self.neighbors = {}  # neighbor_id -> Link
        self.routing_table = {self.id: (0, self.id)}  # destination -> (cost, next_hop)
        self.log = []

    def add_neighbor(self, neighbor_id, link):
        self.neighbors[neighbor_id] = link

    def send_vector(self):
        vector = {dest: cost for dest, (cost, _) in self.routing_table.items()}
        self.log.append(f"[{self.simulator.now()}] Router {self.id} sends vector: {vector}")
        for neighbor_id, link in self.neighbors.items():
            packet = Packet(self.id, vector)
            delay = link.delay(packet.size_bits())
            self.simulator.add_event(delay, lambda rid=neighbor_id, pkt=packet:
                                     self.simulator.routers[rid].receive_vector(pkt))

    def receive_vector(self, packet):
        updated = False
        log_entries = []
        cost_to_sender = self.neighbors[packet.sender_id].cost
        log_entries.append(f"[{self.simulator.now()}] Router {self.id} receives vector from {packet.sender_id}: {packet.vector}")
        for dest, cost in packet.vector.items():
            if dest == self.id:
                continue  # skip route to self
            new_cost = cost + cost_to_sender
            if (dest not in self.routing_table) or (new_cost < self.routing_table[dest][0]):
                old = self.routing_table.get(dest, None)
                self.routing_table[dest] = (new_cost, packet.sender_id)
                updated = True
                if old:
                    reason = f"(updated: old cost {old[0]} via {old[1]})"
                else:
                    reason = "(new route)"
                log_entries.append(f"  -> route to {dest} updated: cost={new_cost}, next_hop={packet.sender_id} {reason}")

        self.log.extend(log_entries)
        if updated:
            self.send_vector()

    def display_routing_table(self):
        print(f"-- Router {self.id} :")
        print("dest cost next-hop")
        for dest, (cost, next_hop) in sorted(self.routing_table.items()):
            print(f"{dest} {cost} {next_hop}")
        print()

    def show_log(self):
        for entry in self.log:
            print(entry)

def load_topology(json_path, simulator):
    with open(json_path, "r") as f:
        data = json.load(f)

    routers = {}
    links = []

    for link in data["links"]:
        r1, r2 = link["endpoints"]
        for r in (r1, r2):
            if r not in routers:
                routers[r] = Router(r, simulator)
        l = Link(r1, r2,
                 link["propagation_speed"],
                 link["transmission_speed"],
                 link["distance"],
                 link["cost"])
        links.append(l)
        routers[r1].add_neighbor(r2, l)
        routers[r2].add_neighbor(r1, l)

    simulator.routers = routers

    if "events" in data:
        for event in data["events"]:
            if event["type"] == "cost_change":
                time_ms = event["time"]
                a, b = event["link"]
                new_cost = event["new_cost"]
                def change_cost():
                    for l in links:
                        if {l.router1, l.router2} == {a, b}:
                            l.cost = new_cost
                            print(f"[{simulator.now()}] Link cost between {a}-{b} changed to {new_cost}")
                            break
                simulator.add_event(time_ms / 1000, change_cost)

    return routers