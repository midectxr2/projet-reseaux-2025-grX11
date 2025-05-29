from network.Packet import Packet
class Routeur:
    def __init__(self, router_id, simulator):
        self.id = router_id
        self.simulator = simulator
        self.neighbors = {}
        self.routing_table = {}
        self.vector = {}
        self.sent_vectors = {}
        self.received_vectors= {}
    
    def add_link(self, neighbor, link):
        self.neighbors[neighbor.id] = link
        self.routing_table[neighbor.id] = (link.cost, neighbor.id)
        self.vector[neighbor.id] = link.cost
        self.log_update()

    def send_vector(self):
        for neighbor_id, link in self.neighbors.items():
            vector = self.vector.copy()

            if self.sent_vectors.get(neighbor_id) != vector:
                packet = Packet(self.id, neighbor_id, vector)
                link.transmit(packet,self.id)
                self.sent_vectors[neighbor_id] = vector.copy()


    def receive_vector(self, id, vector):
        self.received_vectors[id] = vector

        dests = set(self.vector.keys())

        for vec in self.received_vectors.values():
            dests.update(vec.keys())

        new_routing_table = {}
        new_vector = {}


        for dest in dests:
            if dest == self.id:
                continue
            
            best_cost=float('inf')
            best_next_hop=None
            
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
                new_vector[dest] = best_cost

        if new_vector != self.vector:
            self.routing_table = new_routing_table
            self.vector = new_vector
            self.log_update()
            self.send_vector()
        
    def log_update(self):
        print(f"@{self.simulator.now():.3f}s Router {self.id} updated its routing table:")
        for dest, (cost, next_hop) in self.routing_table.items():
            print(f"  {dest} via {next_hop} cost {cost}")
    
