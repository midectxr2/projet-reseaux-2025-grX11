from Simulator import Simulator
from network.Routeur import *

# Initialiser le simulateur
sim = Simulator()

# Charger la topologie depuis un fichier JSON
routers = load_topology("topologies/topo_validation_5r_7l.json", sim)


#test pour debug
'''print("=== Vérification des liens chargés ===")
for r in routers.values():
    for nid, link in r.neighbors.items():
        print(f"Routeur {r.id} - voisin {nid} | coût : {link.cost}")
'''

# Chaque routeur envoie son vecteur initial
for r in routers.values():
    sim.add_event(0, r.send_vector)

# Lancer la simulation
sim.run()

# Afficher les tables de routage finales
for r in sorted(routers.values(), key=lambda x: x.id):
    r.display_routing_table()

# (Optionnel) Afficher les logs de chaque routeur
for r in sorted(routers.values(), key=lambda x: x.id):
    r.show_log()
