__author__ = 'n3k'

from Logger import Logger
from abc import ABCMeta, abstractmethod

class Subject(object):

    __metaclass__ = ABCMeta

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

    @abstractmethod
    def notify(self, params={}):
        pass



class InterruptMechanism(Subject):

    def __init__(self):
        super(InterruptMechanism,self).__init__()


class Clock(Subject):

    def __init__(self):
        super(Clock,self).__init__()
        self._clock_value = 0
        self.clock = self.__next_clock_cycle()

    def notify(self, params={}):
        for observer in self._observers:
            observer.update(params["clock"])

    def read_system_clock(self):
        return self._clock_value

    def __next_clock_cycle(self):
        """Generator"""
        cycle = 0
        while True:
            self._clock_value = cycle
            Logger().log(["Time: {0}".format(self._clock_value)])
            self.notify({"clock" : self._clock_value})
            yield cycle
            cycle += 1

    def tick(self):
        return self.clock.next()