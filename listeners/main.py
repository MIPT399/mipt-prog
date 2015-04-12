from logic.main import EventQueue
import threading as th

children_lock = th.Lock()

__all__ = ['loadAll', 'stopAll', 'pipes', 'children_lock', 'listener']

listeners = []
children = []
pipes = {}


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
        children.append(child)
        child.start()


def stopAll():
    for p in children:
        p.stop()


from . import *