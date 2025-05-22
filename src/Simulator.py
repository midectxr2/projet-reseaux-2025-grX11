import queue


class SimulatorEvent:
    _en = 0

    def __init__(self, time, event):
        """Args:
            time (int): time of execution
            event (callable): function to execute to trigger the event
        """
        self.num = SimulatorEvent._en
        self.time = time
        self.event = event
        SimulatorEvent._en += 1

    def __lt__(self, other):
        return self.time < other.time or (self.time == other.time and self.num < other.num)

    def run(self):
        self.event()


class Simulator:  # REM: Ajouter des logs DEBUG pourraient être utile
    def __init__(self):
        self.reset()

    def add_event(self, delta_t, event):
        """Args:
            delta_t (int): delay before execution, absolute trigger time is now + delta_t
            event (callable): function to execute to trigger the event
        """
        assert delta_t >= 0
        self.q.put(SimulatorEvent(self.__now + delta_t, event))

    def run(self):
        while self.q.qsize() > 0:
            e = self.q.get()
            self.__now = e.time
            e.run()

    def now(self):
        return self.__now

    def reset(self):
        self.__now = 0
        self.q = queue.PriorityQueue()

