class Packet:
    def __init__(self, src, dst, vector):
        self.src = src
        self.dst = dst
        self.vector = vector

    def size_bits(self):
        return len(self.vector) * 32 
