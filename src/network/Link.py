class Link:
    def __init__(self, router1, router2, propagation_speed, transmission_speed, distance, cost):
        self.router1 = router1
        self.router2 = router2
        self.propagation_speed = propagation_speed
        self.transmission_speed = transmission_speed
        self.distance = distance
        self.cost = cost

    def delay(self, packet_size_bits):
        return self.distance / self.propagation_speed + packet_size_bits / self.transmission_speed

    def other_end(self, router_id):
        return self.router2 if router_id == self.router1 else self.router1
