__author__ = 'n3k'

from Logger import Logger
import sys


class ProcessState(object):

    def __init__(self):
        pass

    def change_state(self, process, clock_value=0):
        pass

    def update(self, process, clock_value=0):
        pass

    def __str__(self):
        pass

class StateNewProcess(ProcessState):
    def change_state(self, process, clock_value=0):
        #Just put the process into ready state
        process.process_operations.execute_change_state(process)
        Logger().log(["Process {0} in READY State at time {1}".format(process.pid, clock_value)])

    def update(self, process, clock_value=0):
        Logger().log(["Process {0} in NEW State at time {1}".format(process.pid, clock_value)])
        process.start_time =  clock_value
        # this is used for the shor-term scheduler
        process.last_device_executed_time["CPU"] = clock_value
        # Change state to Ready
        process.change_state(clock_value)

    def __str__(self):
        return "NewProcess"

#Only the short-term-scheduler controls this state
class StateReadyProcess(ProcessState):

    device_name = "CPU"

    def change_state(self, process, clock_value=0):

        if process.previous_state is process.new_process or process.previous_state is process.io_execution_process:
            process.previous_state = process.ready_process
            process.state = process.cpu_execution_process
            Logger().log(["Process {0} in Execution-State at time {1}".format(process.pid, clock_value)])

        elif process.previous_state is process.cpu_execution_process:
            # process was previously preempted
            process.previous_state = process.ready_process
            process.state = process.cpu_execution_process
            Logger().log(["Process {0} in Execution-State at time {1}".format(process.pid, clock_value)])

        else:
            Logger().log(["Something weird just happened"])
            sys.exit(-1)

    def update(self, process, clock_value=0):
        Logger().log(["Process {0} is waiting for CPU at time {1}".format(process.pid,clock_value)])
        process.wait_device_time[self.device_name] += 1
        # The short-term-scheduler is the one who calls change_state() in this case

    def __str__(self):
        return "ReadyProcess"


class StateCPUExecutionProcess(ProcessState):

    device_name = "CPU"

    def change_state(self, process, clock_value=0):
        process.previous_state = process.cpu_execution_process
        if process.device_work_units[self.device_name] > 0:
            # Process is being preempted
            Logger().log(["Process {0} CPU-Preempted".format(process.pid)])
            process.state = process.ready_process

        else:
            process.process_operations.execute_change_state(process)

    def update(self, process, clock_value=0):
        process.device_execution_time[self.device_name] += 1
        process.last_device_executed_time[self.device_name] = clock_value
        Logger().log(["Process {0} executed at time {1}".format(process.pid, clock_value)])
        result = process.process_device_unit(self.device_name)
        if not result :
            Logger().log(["Error (CPUStateExecution): this shouldn't have happened"])
            sys.exit(-1)

    def __str__(self):
        return "CPUExecutionProcess"


class StateBlockedProcess(ProcessState):

    device_name = "DISK"

    def change_state(self, process, clock_value=0):

        if process.previous_state is process.cpu_execution_process:
            process.previous_state = process.blocked_process
            process.state = process.io_execution_process
            Logger().log(["Process {0} in IO-Execution State".format(process.pid)])

        elif process.previous_state is process.io_execution_process:
            # process was previously preempted
            process.previous_state = process.blocked_process
            process.state = process.io_execution_process
            Logger().log(["Process {0} in IO-Execution State".format(process.pid)])

        else:
            Logger().log(["Something weird just happened"])
            sys.exit(-1)

    def update(self, process, clock_value=0):
        process.wait_device_time[self.device_name] += 1

    def __str__(self):
        return "BlockedProcess"


class StateIOExecutionProcess(ProcessState):

    device_name = "DISK"

    def change_state(self, process, clock_value=0):
        process.previous_state = process.io_execution_process
        if process.device_work_units[self.device_name] > 0:
            # Process is being preempted
            # Currently this state shouldn't be reached, given it's FCFS only
            process.state = process.blocked_process
            Logger().log(["Process {0} IO-Preempted".format(process.pid)])
        else: # Process has finished its IO task and now goes back to ready-state for CPU processing
            process.process_operations.execute_change_state(process)
            Logger().log(["Process {0} Ready-State".format(process.pid)])

    def update(self, process, clock_value=0):
        process.device_execution_time[self.device_name] += 1
        result = process.process_device_unit(self.device_name)
        if not result :
            process.last_device_executed_time[self.device_name] = clock_value
            process.change_state(clock_value==clock_value)
            Logger().log(["Process {0} Finished IO at time {1}".format(process.pid,clock_value)])
        else:
            Logger().log(["Process {0} IO-Executed at time {1}".format(process.pid,clock_value)])

    def __str__(self):
        return "IOExecutionProcess"

class StateExitProcess(ProcessState):

    def change_state(self, process, clock_value=0):
        pass

    def update(self, process, clock_value=0):
        Logger().log(["Process {0} Finished at time {1}".format(process.pid,clock_value)])
        process.return_time = clock_value - process.start_time # CHECK IF THIS IS THE CORRECT DEFINITION OF RETURN TIME..
        manager = process.system_manager
        manager.system_clock.detach(process)

    def __str__(self):
        return "ExitProcess"

class Process(object):

    new_process = StateNewProcess()
    ready_process = StateReadyProcess()
    blocked_process = StateBlockedProcess()
    cpu_execution_process = StateCPUExecutionProcess()
    io_execution_process = StateIOExecutionProcess()
    exit_process = StateExitProcess()

    def __init__(self, pid, priority=5, process_operations=None, systemManager=None):

        self.pid = pid
        self.priority = priority
        self.system_manager = systemManager

        self.process_operations = process_operations

        self.cpu_execution_time_instances = []

        self.device_work_units = dict( (k,0) for k in self.system_manager.devices )
        self.last_device_executed_time = dict( (k,0) for k in self.system_manager.devices )
        self.device_execution_time = dict( (k,0) for k in self.system_manager.devices )
        self.wait_device_time = dict( (k,0) for k in self.system_manager.devices )

        self.start_time = 0
        self.return_time = 0
        self.total_time = 0

        self.state = self.new_process
        self.previous_state = None

    def __str__(self):
        return "Process PID: {0} - State: {1}".format(self.pid, self.state)

    def process_device_unit(self, device):
        if self.device_work_units[device] > 0:
            self.device_work_units[device] -= 1
            return True
        return False


    def update(self, clock_value):
        self.state.update(self, clock_value)

    def change_state(self, clock_value):
        self.state.change_state(self, clock_value)