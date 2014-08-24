__author__ = 'n3k'

from Logger import Logger

class Subject(object):

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, clock_value):
        for observer in self._observers:
            observer.update(clock_value)


class InterruptMechanism(Subject):

    def __init__(self):
        super(InterruptMechanism,self).__init__()


class Clock(Subject):

    def __init__(self):
        super(Clock,self).__init__()
        self._clock_value = 0
        self.clock = self._next_clock_cycle()

    def read_system_clock(self):
        return self._clock_value

    def _next_clock_cycle(self):
        cycle = 0
        while True:
            self._clock_value = cycle
            Logger.GetInstance().log(["Tiempo: {0}".format(self._clock_value)])
            self.notify(self._clock_value)
            yield cycle
            cycle += 1

    def tick(self):
        return self.clock.next()