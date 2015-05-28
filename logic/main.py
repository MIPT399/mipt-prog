from structures.game import *
import multiprocessing as mp 

EventQueue = mp.Queue()
ARGV = []

from listeners.main import loadAll, stopAll, pipes, children_lock

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


def join(str, listener):
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
		nPlayer = Player(name=str, base={"health" : maxBaseHealth, "position" : nPos}, units=[], listener=listener, waiting=False)
		Players.append(nPlayer)
		return Response(result = True)


def getField():
		return Players


def moveUnit(action):
		if action.owner not in [player.name for player in Players]:
				return Response(result = False, cause = 'You should first join with this nickname')
		index = [player.name for player in Players].index(action.owner)
		if action.id not in [unit.id for unit in Players[index].units]:
				return Response(result = False, cause = 'The unit with this id wasn\'t found')
		unitIndex = [unit.id for unit in Players[index].units].index(action.id)
		player = Players[index]
		if abs(action.position.x - player.units[unitIndex].position.x) + abs(action.position.y - player.units[unitIndex].position.y) != 1:
				return Response(result = False, cause = 'This cell is not available')
		Players[index].units[unitIndex].position = action.position
		return Response(result = True)


def attack(action):
		if  action.owner not in [player.name for player in Players]:
				return Response(result = False, cause = 'You should first join with this nickname')
		index = [player.name for player in Players].index(action.owner)
		player = Players[index]
		if action.id not in player.units:
				return Response(result = False, cause = 'There is no alive unit with this id')
		unitIndex = [unit.id for unit in player.units].index(action.id)
		if abs(action.position.x - player.units[unitIndex].position.x) + abs(action.position.y - player.units[unitIndex].position.y) > 1:
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

def disconnect(action):
		name = str(action)
		if name not in [player.name for player in Players]:
				return Response(result = False, cause = 'You do not exist')
		index = [player.name for player in Players].index(name)
		Players[index].base["health"] = 0
		Players[index].units = []
		return Response(result = True)

def makeNewTurn():
		for i in range(len(Players)):
				if Players[i].base["health"] > 0:
						uniqueId = 0
						ids = [unit.id for unit in Players[i].units]
						while str(uniqueId) in ids:
								uniqueId += 1
						Players[i].units.append(Unit(id = str(uniqueId), position = Players[i].base["position"], health = maxUnitHealth))


def answer(to, obj):
	children_lock.acquire()
	try:
		pipes[to].send(obj)
	finally:
		children_lock.release()


def main(args):
		global currentPlayer, ARGV
		ARGV = args
		loadAll()
		#event loop
		while True:
				method, args, listener = EventQueue.get()
				newPlayerTurn = True
				print(method, args)
				if method == 'stop':
						stopAll()
						break
				elif method != 'join' and len(Players) < maxPlayersCount:
						answer(listener, Response(result = False, cause = 'It is necessary to wait for other players'))
				elif method == 'join':
						answer(listener, join(args, listener))
				elif method == 'disconnect':
						answer(listener, disconnect(args))
				elif method == 'getField':
						answer(listener, getField())
						newPlayerTurn = False
				elif method == 'wait':
						index = [x.name for x in Players].index(args.owner)
						Players[index].waiting = True
						newPlayerTurn = False						
				elif method == 'moveUnit':
						if Players[currentPlayer].name != args.owner:
							answer(listener, Response(result = False, cause = 'Please wait for your turn'))
						else:
							answer(listener, moveUnit(args))
				elif method == 'attack':
						if Players[currentPlayer].name != args.owner:
							answer(listener, Response(result = False, cause = 'Please wait for your turn'))
						else:
							answer(listener, attack(args))
				else:
						print('Unknown method')

				if newPlayerTurn and len(Players) > 0:
						currentPlayer = (currentPlayer + 1) % len(Players)
						while Players[currentPlayer].base["health"] <= 0 and len(Players[currentPlayer].units) == 0:
								currentPlayer = (currentPlayer + 1) % len(Players)
								if currentPlayer == 0:
										makeNewTurn()
						if Players[currentPlayer].waiting:
								answer(Players[currentPlayer].listener, Response(result = True))
								Players[currentPlayer].waiting = False