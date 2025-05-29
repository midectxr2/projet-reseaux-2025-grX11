class Link:
    def __init__(self, r1, r2, distance, p_speed, t_speed, cost, simulator):
        self.routers = (r1, r2) 
        self.distance = distance
        self.p_speed = p_speed
        self.t_speed = t_speed
        self.cost = cost
        self.simulator = simulator

    def transmit(self, packet, id):
        if self.routers[0].id == id:
            dst = self.routers[1]
        else:
            dst = self.routers[0]

        message_size = packet.size_bits()
        delay = self.distance / self.p_speed + message_size / self.t_speed
        self.simulator.add_event(delay, lambda dst=dst, id=id, packet=packet :self.deliver(dst, id, packet))

    def deliver(self, dst, id ,packet):
        dst.receive_vector(id, packet.vector)
        



        
                    