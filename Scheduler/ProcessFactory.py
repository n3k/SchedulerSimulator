__author__ = 'n3k'

from Process import Process
from Operation import *
from random import randrange

class ProcessFactory(object):

    def __init__(self, systemManager):
        self.system_manager = systemManager
        self._generate_pid = self._get_next_pid()
        self._devices_list = self.system_manager.io_devices.keys()

    # PIDs Generator
    def _get_next_pid(self):
        pid = 1
        while True:
            yield pid
            pid += 1

    def _create_cpu_operation(self):
        units = randrange(1,16)
        return CPUOperation(units)

    def _create_io_operation(self,device):
        units = randrange(1,9)
        return IOOperation(device, units)

    def _generate_operations_vector(self, cpu_bursts, io_bursts):

        vector = []

        for i in range(0,cpu_bursts+io_bursts):
            if i == 0:
                vector.append(self._create_cpu_operation())
            elif i & 1:
                device_index = randrange(0, len(self.system_manager.io_devices))
                device = self._devices_list[device_index]
                vector.append(self._create_io_operation(device))
            else:
                 vector.append(self._create_cpu_operation())

        return vector


    def create_process(self):
        priority = randrange(0, 6)
        pid = self._generate_pid.next()

        cpu_bursts = randrange(1, 5)
        io_bursts = cpu_bursts - 1

        composite_operation = CompositeOperation()

        for operation in self._generate_operations_vector(cpu_bursts, io_bursts):
            composite_operation.add_operation(operation)

        process = Process(pid, priority, composite_operation, systemManager=self.system_manager)

        return process
    """
    def create_process(self):
        priority = randrange(0,6)
        pid = self._generate_pid.next()


        composite_operation = CompositeOperation()

        composite_operation.add_operation(CPUOperation(5))
        composite_operation.add_operation(IOOperation("DISK",5))
        composite_operation.add_operation(CPUOperation(4))

        process = Process(pid,priority,composite_operation ,systemManager=self.system_manager)

        return process
    """