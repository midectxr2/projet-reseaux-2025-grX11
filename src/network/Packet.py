class Packet:
    def __init__(self, sender_id, vector):
        self.sender_id = sender_id
        self.vector = vector  # {destination: cost}

    def size_bits(self):
        return len(self.vector) * 32  # exemple : 32 bits par entrée
