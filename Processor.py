__author__ = 'n3k'

import threading
from time import sleep
from Logger import Logger

class Processor(threading.Thread):

    def __init__(self, systemManager, queue):
        threading.Thread.__init__(self)
        self.stop_request = threading.Event()
        self.system_manager = systemManager
        self.queue = queue
        self.idle_time_points = []
        self.interrupt = False

    def update(self, interrupt):
        self.interrupt = interrupt

    def join(self, timeout=None):
        self.stop_request.set()
        super(Processor, self).join(timeout)

    def __update_processes_cpu_time_instances(self):
        for p in self.system_manager.system_process_list:
            if p.state is p.cpu_execution_process:
                p.cpu_execution_time_instances.append(1)
            else:
                p.cpu_execution_time_instances.append(0)

    def __adjust_processes_cpu_time_instances(self):
        """This method inserts zeros at the cpu_time_instances list of those processes
        that were created when the simulator was already running. This adjust the list
        in a way of saying that a given processes was not being executed at the time"""
        cpu_instaces_list = [p.cpu_execution_time_instances for p in self.system_manager.system_process_list]
        for p in self.system_manager.system_process_list:
            while len(p.cpu_execution_time_instances) < len(max(cpu_instaces_list, key=len)):
                p.cpu_execution_time_instances.insert(0,0)

    def process_task(self, process):

        while process.device_work_units["CPU"] > 0 and self.interrupt == False:
            Logger().log(["AND THE CURRENT PROCESS IS: {0} and is in {1}".format(process.pid, process.state)])
            self.system_manager.system_clock.tick()
            self.__update_processes_cpu_time_instances()


    def process_ready_execution_exists(self):
        # The scheduler puts the process in execution state, but it's the job
        # of the Processor to really grab it and execute it
        for p in self.system_manager.system_process_list:
            if p.state is p.ready_process or p.state is p.cpu_execution_process:
                return True
        return False


    def run(self):
        sleep(3) # for slow-start xD
        while not self.stop_request.is_set():
            # PROCESSOR IDLE
            while not self.process_ready_execution_exists() and not self.stop_request.is_set():
                sleep(1)
                self.system_manager.system_clock.tick()
                self.__update_processes_cpu_time_instances()
                self.idle_time_points.append(self.system_manager.system_clock.read_system_clock())
                Logger().log([self.idle_time_points])

            if not self.stop_request.is_set():
                process = self.queue.get()
                self.process_task(process) #process TASK and clock.next() for every processed unit
                self.queue.task_done()
                sleep(1)

        self.__adjust_processes_cpu_time_instances()
