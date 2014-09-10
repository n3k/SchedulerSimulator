__author__ = 'n3k'

import threading
from Singleton import Singleton

class Logger(object):

    __metaclass__ = Singleton

    def __init__(self):
        self.logfile = "c:\\logfile.txt"
        with open(self.logfile, "w") as f:
            f.write("Here is the logged information\n")
            f.write("---------------------------------------------------\n")

    def log(self, lines=[]):
        with open(self.logfile, "a") as f:
            for line in lines:
                f.writelines("{0}\n".format(line))

