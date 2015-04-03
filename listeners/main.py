from logic.main import EventQueue
import multiprocessing as mp

__all__ = ['loadAll', 'stopAll', 'pipes']

listeners = []
children = []
pipes = {}

def listener(cls, name):
    listeners.append((name, cls))
    pipes[name] = mp.Pipe()
    return cls

def loadAll():
    for i in range(len(listeners)):
        name, cls = listeners[i]
        obj = cls(EventQueue)
        listeners[i] = (name, obj)
        p = mp.Process(target=obj.main)
        children.append(p)
        p.start()

def stopAll():
    for p in children:
        p.stop()
