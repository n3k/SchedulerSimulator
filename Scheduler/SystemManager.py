__author__ = 'n3k'

from IODevice import IODevice
from Clock import Clock
from Logger import Logger
from Scheduler import *
from datetime import datetime
import Queue


class SystemManager(object):

    def __init__(self):

        self.timer = 10

        self.init_time = datetime.now()
        self.system_clock = Clock()
        self.interrupt_mechanism = None
        self.processor = None
        self.processor_task_queue = Queue.Queue(maxsize=1)
        self.longScheduler = None
        self.shortScheduler = None
        self.max_system_processes = 5
        self.system_process_list = []

        self.devices = {"CPU" : None, "DISK" : None} #, "GRAPHIC" : None}
        self.io_devices = self.devices.copy()
        del self.io_devices["CPU"]



    def start_processor(self):
        #self.interrupt_mechanism = InterruptMechanism()
        self.processor = Processor(systemManager=self, queue=self.processor_task_queue)
        self.devices["CPU"] = self.processor
        #self.interrupt_mechanism.attach(observer=self.processor)
        self.processor.setDaemon(True)
        self.processor.start()
        Logger().log(["Processor Started"])

    def start_long_scheduler(self):
        self.longScheduler = LongTermScheduler(systemManager=self, processList=self.system_process_list)
        self.longScheduler.setDaemon(True)
        self.longScheduler.start()
        Logger().log(["Long-Term Scheduler Started"])

    def start_short_scheduler(self):
        self.shortScheduler = FCFS(systemManager=self,processList=self.system_process_list)
        self.shortScheduler.setDaemon(True)
        self.shortScheduler.start()
        Logger().log(["Short-Term Scheduler Started"])

    def start_io_device(self, device):
        self.devices[device] = IODevice(device, systemManager=self,processList=self.system_process_list)
        self.devices[device].setDaemon(True)
        self.devices[device].start()
        Logger().log(["{0} Device Started".format(device)])

    def start_system_device(self, device):
        if device == "CPU":
            self.start_processor()
        else:
            self.start_io_device(device)


    def check_all_process_finished(self):
        for p in self.system_process_list:
            if p.state != p.exit_process:
                return False
        return True

    def run(self):
        self.start_long_scheduler()
        self.start_short_scheduler()
        for k in self.devices:
            self.start_system_device(k)


        sleep(self.timer*2)
        self.longScheduler.join()

        while not self.check_all_process_finished():
            sleep(3)

        self.shortScheduler.join()
        for k, v in self.devices.items():
            if k != "CPU":
                v.join()
        self.processor.join()

        # Now we need to plot the CPU Usage

        print "Exitting Application"



