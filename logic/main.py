import sys
from structures.game import *
import multiprocessing as mp 
from . import *

EventQueue = mp.Queue()

from listeners.main import loadAll, stopAll, pipes

__all__ = ['main', 'EventQueue']

Players = []

__last_base_location = Point(x=0, y=0)

def genNewBase():
    return

def join(str):
    pass

def getField():
    pass

def moveUnit(action):
    pass

def attack(action):
    pass

def answer(to, obj):
    pipes[to].send(obj)

def main(args):
    loadAll()
    #event loop
    while True:
        method, args, listener = EventQueue.get()
        if method == 'join':
            answer(listener, join(args))
        elif method == 'getField':
            answer(listener, getField())
        elif method == 'moveUnit':
            answer(listener, moveUnit(args))
        elif method == 'attack':
            answer(listener, attack(args))
        elif method == 'stop':
            stopAll()
            break
        else:
            print('Unknown method')

