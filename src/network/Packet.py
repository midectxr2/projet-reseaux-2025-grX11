class Packet:
    def __init__(self, src, dst, vector):
        self.src = src
        self.dst = dst
        self.vector = vector  # dict {dest: cost}

    def size_bits(self):
        return len(self.vector) * 32  # suppose 32 bits (4 octets) par entrée
