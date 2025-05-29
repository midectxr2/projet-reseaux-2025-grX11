from network.Packet import Packet
class Routeur:
    def __init__(self, router_id, simulator):
        self.id = router_id
        self.simulator = simulator
        self.neighbors = {}
        self.routing_table = {}
        self.distance_vector = {}
        self.sent_vectors = {}
        self.received_vectors= {}
    
    def add_link(self, neighbor, link):
        self.neighbors[neighbor.id] = link
        self.routing_table[neighbor.id] = (link.cost, neighbor.id)
        self.distance_vector[neighbor.id] = link.cost

    def send_distance_vector(self):
        for neighbor_id, link in self.neighbors.items():
            vector = self.distance_vector.copy()

            if self.last_sent_vectors.get(neighbor_id) != vector:
                packet = Packet(self.id, neighbor_id, vector)
                link.transmit(packet, from_router_id=self.id)
                self.last_sent_vectors[neighbor_id] = vector.copy()


    def receive_vector(self, from_id, vector):
        self.received_vectors[from_id] = vector

        all_dests = set(self.distance_vector.keys())
        for vec in self.received_vectors.values():
            all_dests.update(vec.keys())

        new_routing_table = {}
        new_distance_vector = {}

        for dest in all_dests:
            if dest == self.id:
                continue

            if dest in self.neighbors:
                direct_cost = self.neighbors[dest].cost
                if direct_cost < best_cost:
                    best_cost = direct_cost
                    best_next_hop = dest

            for neighbor_id, link in self.neighbors.items():
                neighbor_vector = self.received_vectors.get(neighbor_id, {})
                if dest in neighbor_vector:
                    cost_via_neighbor = link.cost + neighbor_vector[dest]
                    if cost_via_neighbor < best_cost:
                        best_cost = cost_via_neighbor
                        best_next_hop = neighbor_id

            if best_next_hop is not None:
                new_routing_table[dest] = (best_cost, best_next_hop)
                new_distance_vector[dest] = best_cost

        
        self.routing_table = new_routing_table
        self.distance_vector = new_distance_vector
            
        self.send_distance_vector()
        self.log_update()




    def log_update(self):
        print(f"@{self.simulator.now():.3f}s Router {self.id} updated its routing table:")
        for dest, (cost, next_hop) in self.routing_table.items():
            print(f"  {dest} via {next_hop} cost {cost}")
    
    def notify_link_cost_change(self, neighbor_id, new_cost):
    # Met à jour le coût direct vers le voisin
        if neighbor_id in self.routing_table:
            self.routing_table[neighbor_id] = (new_cost, neighbor_id)
            self.distance_vector[neighbor_id] = new_cost

        updated = False
        for dest, (cost, next_hop) in list(self.routing_table.items()):
            if next_hop == neighbor_id:
                # recalcul potentiel
                alt_cost = self.neighbors[neighbor_id].cost + self.distance_vector.get(dest, float('inf'))
                if alt_cost != cost:
                    self.routing_table[dest] = (alt_cost, neighbor_id)
                    self.distance_vector[dest] = alt_cost
                    updated = True

        if updated:
            self.log_update()
            self.send_distance_vector()

