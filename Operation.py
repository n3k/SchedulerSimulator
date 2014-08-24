__author__ = 'n3k'

from abc import ABCMeta,abstractmethod

class Operation(object):

    __metaclass__ = ABCMeta

    def __init__(self, units=0):
        self.units = units

    @abstractmethod
    def execute_change_state(self,process):
        pass

    @abstractmethod
    def add_operation(self, operation):
        pass

    @abstractmethod
    def remove_operation(self, operation):
        pass

    @abstractmethod
    def describe(self):
        pass


class CompositeOperation(Operation):

    def __init__(self, units=0):
        super(CompositeOperation,self).__init__(units)
        self.operations = []

    def add_operation(self,operation):
        self.operations.append(operation)

    def remove_operation(self,operation):
        self.operations.remove(operation)

    def select_operation(self):
        try:
            operation = self.operations.pop(0)
        except:
            return None
        return operation

    def execute_change_state(self, process):
        operation = self.select_operation()
        if not operation:
            process.state = process.exit_process
        else:
            operation.execute_change_state(process)

    def describe(self):
        message = "Process Operations:\n"
        for op in self.operations:
            message += "{0}\n".format(op.describe())
        return message


class CPUOperation(Operation):

    def __init__(self, units=0):
        super(CPUOperation,self).__init__(units)
        self.device = "CPU"

    def execute_change_state(self,process):
        process.previous_state = process.state
        process.state = process.ready_process
        process.device_work_units[self.device] = self.units

    def add_operation(self, operation):
        pass

    def remove_operation(self, operation):
        pass

    def describe(self):
        return "Device: {0} - Units: {1}".format(self.device,self.units)


class IOOperation(Operation):

    def __init__(self, device, units=0):
        super(IOOperation,self).__init__(units)
        self.device = device

    def execute_change_state(self,process):
        process.previous_state = process.state
        process.state = process.blocked_process
        process.device_work_units[self.device] = self.units

    def add_operation(self, operation):
        pass

    def remove_operation(self, operation):
        pass

    def describe(self):
        return "Device: {0} - Units: {1}".format(self.device,self.units)