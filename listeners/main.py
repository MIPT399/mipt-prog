from logic.main import EventQueue
import threading as th

children_lock = th.Lock()

__all__ = ['loadAll', 'stop', 'pipes', 'children_lock', 'listener']

listeners = []
children = {}
pipes = {}
status = {}


def listener(name):
    def result(cls):
        listeners.append((name, cls))
        return cls
    return result


def loadAll():
    for i in range(len(listeners)):
        name, cls = listeners[i]
        obj = cls(EventQueue)
        listeners[i] = (name, obj)
        child = th.Thread(target=obj.main)
        child.start()


def stop(listener, message):
    children_lock.acquire()
    try:
        status[listener] = message
        children[listener].terminate()
        del children[listener]
        del pipes[listener]
    finally:
        children_lock.release()

from . import *