import lorem
from Simulator import Simulator

#
#    Router A  | ----------------- | Router B
#
prop_speed = 5e6  # m/s
trans_speed = 1e19  # bps
dist = 1e3  # m


def A_send_to_B(msg):
    print(f"@{sim.now():.3f}s Host A sending message to Host B: '{msg}'")
    delay = dist / prop_speed + len(msg) * 8 / trans_speed
    sim.add_event(delay, lambda: B_receive_from_A(msg))


def B_receive_from_A(msg):
    print(f"@{sim.now():.3f}s Host B received message from Host A: '{msg}'")
    print(f"@{sim.now():.3f}s Host B sending ACK to Host A")
    ack_msg = f"ACK: '{msg}'"
    delay = dist / prop_speed + len(ack_msg) * 8 / trans_speed
    sim.add_event(delay, lambda: A_receive_from_B(ack_msg))


def A_receive_from_B(msg):
    print(f"@{sim.now():.3f}s Host A received message from Host B: '{msg}'")


sim = Simulator()

for i in range(5):
    msg = lorem.sentence()
    sim.add_event(5 * i, lambda: A_send_to_B(msg))

sim.run()