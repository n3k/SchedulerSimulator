__author__ = 'n3k'

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import SystemManager


def fill_process_matrix(process_list):
    # First column is time and other columns represent processes
    # Each row is a clock time
    t = len(process_list[0].cpu_execution_time_instances)
    matrix = np.zeros((len(process_list) + 1) * t ).reshape((t, len(process_list) + 1 ))
    matrix[:, 0] = np.array(range(t))
    for i in xrange(0,len(process_list)):
        matrix[:,i+1] = np.array(process_list[i].cpu_execution_time_instances)

    return matrix

def get_color():
    colours = ["blue", "green", "red", "cyan", "magenta", "yellow", "black"]
    index = 0
    while True:
        yield colours[index%len(colours)]
        index += 1

def make_processes_cpu_plot(matrix):
    # shape[1] returns the number of columns
    colours = get_color()
    plt.subplot(2,1,1)
    plt.ylim(0.1, 1.5)
    plt.xlabel("time(cycles)")
    plt.ylabel("processes")
    for col in xrange(1, matrix.shape[1]):
        color = colours.next()
        plt.figtext(0.1 + (col - 1)*0.02, 0.03, "P{}".format(col), style="italic", bbox={ "facecolor" : color , "alpha" : 0.5 })
        plt.plot(matrix[:,0], matrix[:,col], color[0]+"o")


def make_cpu_usage_plot(cpu_idle_times):
    usage = []
    aux = 0
    for time in cpu_idle_times:
        while aux < time:
            usage.append(1)
            aux += 1
        usage.append(0)
        aux += 1

    plt.subplot(2,1,2)
    plt.xlabel("time(cycles)")
    plt.ylabel("processor")
    plt.ylim(-0.2,1.2)
    plt.plot(range(len(usage)),usage, "ko-")


def make_plot(manager):

    plt.title("CPU USAGE")
    matrix = fill_process_matrix(manager.system_process_list)
    make_processes_cpu_plot(matrix)
    make_cpu_usage_plot(manager.processor.idle_time_points)
    plt.show()


def main():
    manager = SystemManager.SystemManager()
    manager.run()
    make_plot(manager)

if __name__ == "__main__":
    main()