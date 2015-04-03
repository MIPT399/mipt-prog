from logic.main import EventQueue
import multiprocessing as mp

__all__ = ['loadAll', 'stopAll', 'pipes']

listeners = []
children = []
pipes = {}

def listener(name):
    def result(cls):
        listeners.append((name, cls))
        pipes[name] = mp.Pipe()
        return cls
    return result

def loadAll():
    for i in range(len(listeners)):
        name, cls = listeners[i]
        ppipe, cpipe = pipes[name]
        pipes[name] = ppipe
        obj = cls(EventQueue, cpipe)
        listeners[i] = (name, obj)
        p = mp.Process(target=obj.main)
        children.append(p)
        p.start()

def stopAll():
    for p in children:
        p.stop()
