import sys
from structures.game import *
import multiprocessing as mp 

EventQueue = mp.Queue()
ARGV=[]

from listeners.main import loadAll, stopAll, pipes

__all__ = ['main', 'EventQueue', 'ARGV']

maxPlayersCount = 2
maxNicknameLength = 20
maxBaseHealth = 100
maxUnitHealth = 10
maxCoordinate = 20
attackValue = 1
Players = []

currentPlayer = 0

def genNewBase():
        return

def join(str):
        if str in [player.name for player in Players]:
                return Response(result = False, cause = 'This nickname is busy now, try another one')
        if len(Players) >= maxPlayersCount:
                return Response(result = False, cause = 'The server is full, try another one')
        if len(str) > maxNicknameLength:
                return Response(result = False, cause = 'Your nickname is too long, please make it shorter')
        if len(str) < 1:
                return Response(result = False, cause = 'Your nickname is too short, return back after it grows')
        from random import randint
        nPos = Point(x = randint(-maxCoordinate, maxCoordinate), y = randint(-maxCoordinate, maxCoordinate))
        while nPos in [player.base['position'] for player in Players]:
                nPos = Point(x = randint(-maxCoordinate, maxCoordinate), y = randint(-maxCoordinate, maxCoordinate))
        nPlayer = Player(str, {"health" : maxBaseHealth, "position" : nPos}, [])
        return Response(result = True)

def getField():
        return Players

def moveUnit(action):
        if not action.owner in [player.name for player in Players]:
                return Response(result = False, cause = 'You should first join with this nickname')
        index = [player.name for player in Players].index(action.owner)
        player = Players[index]
        if abs(action.position.x - player.units[action.id].position.x) + abs(action.position.y - player.units[action.id].position.y) != 1:
                return Response(result = False, cause = 'This cell is not available')
        Players[index].units[action.id].position = action.position
        return Response(result = True)

def attack(action):
        if not action.owner in [player.name for player in Players]:
                return Response(result = False, cause = 'You should first join with this nickname')
        index = [player.name for player in Players].index(action.owner)
        player = Players[index]
        if not action.id in player.units:
                return Response(result = False, cause = 'There is no alive unit with this id')
        if abs(action.position.x - player.units[action.id].position.x) + abs(action.position.y - player.units[action.id].position.y) > 1:
                return Response(result = False, cause = 'This cell is not available')
        for i in range(len(Players)):
                for j in range(len(Players[i].units)):
                        if Players[i].units[j].id == action.id:
                                Players[i].units[j].health -= attackValue
                                if (Players[i].units[j].health <= 0):
                                        del Players[i].units[j]
                if Players[i].base["position"] == action.position:
                        Players[i].base["health"] -= attackValue
        return Response(result = True)

def makeNewStep():
        for i in range(len(Players)):
                if Players[i].base["health"] > 0:
                        unniqueId = 0
                        ids = [unit.id for unit in Players[i].units]
                        while str(uniqueId) in ids:
                                uniqueId += 1
                        Players[i].units.append(Unit(id = uniqueId, position = Players[i].base["position"], health = maxUnitHealth))

def answer(to, obj):
        pipes[to].send(obj)

def main(args):
        ARGV = args
        loadAll()
        #event loop
        while True:
                method, args, listener = EventQueue.get()
                if method == 'stop':
                        stopAll()
                        break
                elif method != 'join' and len(Players) < maxPlayersCount:
                        answer(listener, Response(result = False, cause = 'It is necessary to wait for other players'))
                elif Players[currentPlayer].name != args.owner:
                        answer(listener, Response(result = False, cause = 'Please wait for your turn'))
                else:
                        if method == 'join':
                                answer(listener, join(args))
                        elif method == 'getField':
                                answer(listener, getField())
                        elif method == 'moveUnit':
                                answer(listener, moveUnit(args))
                        elif method == 'attack':
                                answer(listener, attack(args))
                        else:
                                print('Unknown method')
                        currentPlayer += 1
                        if currentPlayer == len(Players):
                                currentPlayer = 0
                                makeNewStep()

