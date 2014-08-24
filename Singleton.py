__author__ = 'n3k'

import threading

"""
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
"""
"""
class Singleton(object):

    _instance = None
    _lock = threading.RLock()

    def __init__(self):
        # Cannot hide ctor, so raise an error from 2nd instantiation
        if (Singleton._instance != None):
            raise("This is a Singleton! use Singleton.GetInstance method")
        Singleton._instance = self

    @staticmethod
    def GetInstance():
        if (Singleton._instance == None):
            Singleton._lock.acquire()
            if (Singleton._instance == None):
                Singleton._instance = Singleton()
            Singleton._lock.release()
        return Singleton._instance
    @staticmethod
    def Reset():
        Singleton._instance = None
"""