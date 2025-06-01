import json
from Simulator import Simulator
from network.Link import Link
from network.Routeur import Routeur


class Network:
    def __init__(self, json_path):
        self.simulator = Simulator()
        self.routers = {}
        self.links = []
        self.topology(json_path)

    def topology(self, json_path):
        with open(json_path) as f:
            data = json.load(f)

        for link in data["links"]:
            r1, r2 = link["endpoints"]
            for id in (r1, r2):
                if id not in self.routers:
                    self.routers[id] = Routeur(id, self.simulator)
        
            link = Link(
                r1=self.routers[r1],
                r2=self.routers[r2],
                distance=link["distance"],
                p_speed=link["propagation_speed"],
                t_speed=link["transmission_speed"],
                cost=link["cost"],
                simulator=self.simulator
            )

            self.links.append(link)
            self.routers[r1].add_link(self.routers[r2], link)
            self.routers[r2].add_link(self.routers[r1], link)


        for event in data.get("events", []):
            if event["type"] == "cost_change":
                t = event["time"]
                r1, r2 = event["link"]
                new_cost = event["new_cost"]
                if new_cost >= 999999:
                    new_cost = float('inf')
                    
                self.simulator.add_event(t/1000.0, lambda r1=r1, r2=r2, c=new_cost: self.change_cost(r1, r2, c))

        for router in self.routers.values():
            self.simulator.add_event(0, router.send)
             

    def change_cost(self, r1, r2, new_cost):
        for link in self.links:
            routers = link.routers
            if {routers[0].id, routers[1].id} == {r1, r2}:
                link.cost = new_cost
                print(f"@{self.simulator.now():.3f}s Link cost between {r1} and {r2} changed to {new_cost}")
                routers[0].send()
                routers[1].send()
                break


    def print_tables(self):
        for router_id in sorted(self.routers):
            router = self.routers[router_id]
            print(f"-- Router {router.id} :")
            print("dest\tcost\tnext-hop")
            for dest_id, (cost, next_hop) in sorted(router.routing_table.items()):
                print(f"{dest_id}\t{cost}\t{next_hop}")
            print()

    def run(self):
        self.simulator.run()
        self.print_tables()

