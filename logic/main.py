import sys
from structures.game import *
import multiprocessing as mp 
from listeners.main import loadAll, stopAll, pipes

__all__ = ['main', 'EventQueue']

Players = []

__last_base_location = Point(x=0, y=0)
EventQueue = mp.Queue()

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
    pipes[to][0].send(obj)

def main(args):
    loadAll()
    #event loop
    while True:
        method, args, listener = EventQueue.get()
        if name == 'join':
            answer(listener, join(args))
        elif name == 'getField':
            answer(listener, getField())
        elif name == 'moveUnit':
            answer(listener, moveUnit(args))
        elif name == 'attack':
            answer(listener, attack(args))
        elif name == 'stop':
            stopAll()
            break
        else:
            print('Unknown method')

