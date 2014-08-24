__author__ = 'n3k'

import threading
from Logger import Logger

#FCFS behaviour
class IODevice(threading.Thread):

    def __init__(self,device, systemManager, processList):
        threading.Thread.__init__(self)
        self.stop_request = threading.Event()
        self.device = device
        self.system_manager = systemManager
        self.process_list = processList
        self.device_process_list = []

    def join(self, timeout=None):
        self.stop_request.set()
        super(IODevice, self).join(timeout)

    def scan_for_blocked_processes(self):
        for p in self.process_list:
            if p.state is p.blocked_process:
                self.device_process_list.append(p)

    def fetch_process_to_execute(self):
        aux = float('Infinity')
        result = None
        Logger.GetInstance().log([c.pid for c in self.device_process_list])
        for p in self.device_process_list:
            if p.last_device_executed_time[self.device] < aux:
                aux = p.last_device_executed_time[self.device]
                result = p
        if result != None:
            self.device_process_list.remove(result)
        return result

    def run(self):

        while not self.stop_request.is_set():
            process = None
            while not process and not self.stop_request.is_set():
                self.scan_for_blocked_processes()
                process = self.fetch_process_to_execute()
            if process != None:
                clock_value = clock_value=self.system_manager.system_clock.read_system_clock()
                process.change_state(clock_value=clock_value)
                while process.device_work_units[self.device] > 0:
                    pass
                try:
                    self.device_process_list.remove(process)
                except:
                    pass