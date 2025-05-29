class Link:
    def __init__(self, r1, r2, distance, prop_speed, trans_speed, cost, simulator):
        self.routers = (r1, r2) 
        self.distance = distance
        self.prop_speed = prop_speed
        self.trans_speed = trans_speed
        self.cost = cost
        self.simulator = simulator

    def transmit(self, packet, from_router_id):
        if self.router_objs[0].id == from_router_id:
            to_router = self.router_objs[1]
        else:
            to_router = self.router_objs[0]

        message_size_bits = packet.size_bits()
        delay = self.distance / self.prop_speed + message_size_bits / self.trans_speed

        def deliver():
            to_router.receive_vector(from_router_id, packet.vector)

        self.simulator.add_event(delay, deliver)
                    