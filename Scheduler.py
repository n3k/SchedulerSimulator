__author__ = 'n3k'


from abc import ABCMeta,abstractmethod
from Processor import *
from time import sleep
from ProcessFactory import ProcessFactory
from random import randrange

class Scheduler(threading.Thread):

    __metaclass__ = ABCMeta

    def __init__(self, systemManager, processList):
        threading.Thread.__init__(self)
        self.stop_request = threading.Event()
        self.system_manager = systemManager
        self.process_list = processList

    @abstractmethod
    def run(self):
        pass

    def join(self, timeout=None):
        self.stop_request.set()
        super(Scheduler, self).join(timeout)

class LongTermScheduler(Scheduler):

    def __init__(self, systemManager, processList, period=5):
        super(LongTermScheduler, self).__init__(systemManager=systemManager, processList=processList)
        self.check_period = period
        self.process_factory = ProcessFactory(systemManager=systemManager)

    def run(self):
        #Check MultiProgramming Status

        while not self.stop_request.is_set():
            if len(self.process_list) < self.system_manager.max_system_processes:
                jobs_count = self.system_manager.max_system_processes - len(self.process_list)
                for i in xrange(0, randrange(jobs_count)):
                    process = self.process_factory.create_process()

                    Logger().log([process.process_operations.__str__()])

                    Logger().log([str(process.process_operations)])

                    self.process_list.append(process) #ProcessList
                    #Attach to system clock
                    self.system_manager.system_clock.attach(process)
                    sleep(self.check_period)
            else:
                sleep(self.check_period*2)

        """

        process = self.process_factory.create_process()
        Logger().log([process.process_operations.describe()])
        self.process_list.append(process) #ProcessList
        #Attach to system clock
        self.system_manager.system_clock.attach(process)

        process = self.process_factory.create_process()
        Logger().log([process.process_operations.describe()])
        self.process_list.append(process) #ProcessList
        #Attach to system clock
        self.system_manager.system_clock.attach(process)

        process = self.process_factory.create_process()
        Logger().log([process.process_operations.describe()])
        self.process_list.append(process) #ProcessList
        #Attach to system clock
        self.system_manager.system_clock.attach(process)
        """

class ShortTermScheduler(Scheduler):

    __metaclass__ = ABCMeta

    def __init__(self, systemManager, processList,):
        super(ShortTermScheduler,self).__init__(systemManager=systemManager,processList=processList)
        self.short_term_process_list = []

    @abstractmethod
    def fetch_process_to_execute(self):
        pass


    def scan_for_ready_processes(self):
        for p in self.process_list:
            if p.state is p.ready_process:
                self.short_term_process_list.append(p)

    @abstractmethod
    def run(self):
        pass


class FCFS(ShortTermScheduler):

    def __init__(self, systemManager, processList):
        super(FCFS,self).__init__(systemManager=systemManager,processList=processList)

    def fetch_process_to_execute(self):
        aux = float('Infinity')
        result = None
        Logger().log([c.pid for c in self.short_term_process_list])
        for p in self.short_term_process_list:
            if p.last_device_executed_time["CPU"] < aux:
                aux = p.last_device_executed_time["CPU"]
                result = p
        if result != None:
            self.short_term_process_list.remove(result)
        return result

    def run(self):
        processor_queue = self.system_manager.processor_task_queue
        clock = self.system_manager.system_clock
        while not self.stop_request.is_set():
            process = None
            while not process and not self.stop_request.is_set():
                self.scan_for_ready_processes()
                process = self.fetch_process_to_execute()
            if process != None:
                process.change_state(clock_value=clock.read_system_clock())
                processor_queue.put(process)
                # FCFS can join() because it doesn't interrupt()
                processor_queue.join()
                process.change_state(clock_value=clock.read_system_clock())
                if process.state is process.exit_process:
                    process.update(clock_value=clock.read_system_clock())
                try:
                    self.short_term_process_list.remove(process)
                except:
                    pass



class RoundRobin(ShortTermScheduler):

    def __init__(self, systemManager, processList,):
        super(RoundRobin,self).__init__(systemManager=systemManager,processList=processList)

    def run(self):
        while True:
            #
            # Interrupt()
            pass





