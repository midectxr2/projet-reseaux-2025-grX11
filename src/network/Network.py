import json
from Simulator import Simulator
from network.Link import Link
from network.Routeur import Routeur

# --- Classes Router, Link, Packet comme définies précédemment ---
# Pour éviter la répétition ici, on suppose que ces classes sont dans ce même fichier
# ou importées proprement via d'autres fichiers Python

# Voici uniquement le "main" de simulation

class Network:
    def __init__(self, json_path):
        self.simulator = Simulator()
        self.routers = {}
        self.links = []
        self.load_topology(json_path)

    def load_topology(self, json_path):
        with open(json_path) as f:
            data = json.load(f)

        # Création des routeurs
        for link in data["links"]:
            r1, r2 = link["endpoints"]
            for r_id in (r1, r2):
                if r_id not in self.routers:
                    self.routers[r_id] = Routeur(r_id, self.simulator)

            # Création du lien
            link = Link(
                router1=r1,
                router2=r2,
                distance=link["distance"],
                prop_speed=link["propagation_speed"],
                trans_speed=link["transmission_speed"],
                cost=link["cost"],
                simulator=self.simulator
            )

            self.links.append(link)
            self.routers[r1].add_link(self.routers[r2], link)
            self.routers[r2].add_link(self.routers[r1], link)


        # Ajout des événements (modification de coûts)
        for event in data.get("events", []):
            if event["type"] == "cost_change":
                t = event["time"]
                r1, r2 = event["link"]
                new_cost = event["new_cost"]
                self.simulator.add_event(t / 1000.0, lambda r1=r1, r2=r2, c=new_cost: self.change_link_cost(r1, r2, c))

        # Début de la simulation: envoi initial des vecteurs
        for router in self.routers.values():
            self.simulator.add_event(0, router.send_distance_vector)

    def change_link_cost(self, r1, r2, new_cost):
        for link in self.links:
            r_objs = link.router_objs
            if {r_objs[0].id, r_objs[1].id} == {r1, r2}:
                link.cost = new_cost
                print(f"@{self.simulator.now():.3f}s Link cost between {r1} and {r2} changed to {new_cost}")
                r_objs[0].notify_link_cost_change(r_objs[1].id, new_cost)
                r_objs[1].notify_link_cost_change(r_objs[0].id, new_cost)
                break

    def run(self):
        self.simulator.run()
        self.display_routing_tables()

    def display_routing_tables(self):
        for router_id in sorted(self.routers):
            router = self.routers[router_id]
            print(f"-- Router {router.id} :")
            print("dest\tcost\tnext-hop")
            for dest_id, (cost, next_hop) in sorted(router.routing_table.items()):
                print(f"{dest_id}\t{cost}\t{next_hop}")
            print()
