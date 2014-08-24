__author__ = 'n3k'

import threading

class Logger(object):

    #__metaclass__ = Singleton

    _instance = None
    _lock = threading.RLock()

    def __init__(self):

        # Cannot hide ctor, so raise an error from 2nd instantiation
        if (Logger._instance != None):
            raise("This is a Singleton! use Singleton.GetInstance method")
        Logger._instance = self

        self.logfile = "/tmp/logfile.txt"
        with open(self.logfile, "w") as f:
            f.write("Here is the logged information\n")
            f.write("---------------------------------------------------\n")

    @staticmethod
    def GetInstance():
        if (Logger._instance == None):
            Logger._lock.acquire()
            if (Logger._instance == None):
                Logger._instance = Logger()
            Logger._lock.release()
        return Logger._instance
    @staticmethod
    def Reset():
        Logger._instance = None

    def log(self, lines=[]):
        with open(self.logfile, "a") as f:
            for line in lines:
                f.writelines("{0}\n".format(line))

