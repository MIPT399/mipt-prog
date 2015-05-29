from logic.main import ARGV
from json import dumps
import multiprocessing as mp
from listeners.main import *
import socket
import structures.game
import visualizer

@listener('visual')
class Visual:
    def __init__(self, EventQueue):
        self.EventQueue = EventQueue
    def main(self):
        children_lock.acquire()
        try:
            cpipe, ppipe = mp.Pipe()
            name = 'Visual'
            pipes[name] = ppipe
            prc = mp.Process(target=visualizer.main, args=(equeue, name, cpipe))
            children[name] = prc
        finally:
            children_lock.release()
        prc.start()
        prc.join()
        children_lock.acquire()
        try:
            del pipes[name]
        finally:
            children_lock.release()
