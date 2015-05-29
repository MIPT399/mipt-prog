from client import *
import random

print('init', client.init())
print('join', client.join("Lesha"))
print('wait', client.wait())

x = client.getField()
sampleAction = {"id" : x[1].units[0].id, "position" : {"x" : x[1].units[0].position.x - 1, "y" : x[1].units[0].position.y}}
print('moveUnit', client.moveUnit(sampleAction))
print('wait', client.wait())

while True:
	y = client.getField()
	if_gone = 0
	t = random.randrange(0, len(y[1].units))
	for unit in y[0].units:
		if unit.position.x == y[1].units[t].position.x and unit.position.y == y[1].units[t].position.y + 1:
			sA_attack = {"id" : y[1].units[t].id, "position" : {"x" :  y[1].units[t].position.x, "y" :  y[1].units[t].position.y + 1}}
			print('attack', client.attack(sA_attack))
			if_gone = 1
			break
		if unit.position.x == y[1].units[t].position.x + 1 and unit.position.y == y[1].units[t].position.y:
			sA_attack = {"id" : y[1].units[t].id, "position" : {"x" :  y[1].units[t].position.x + 1, "y" :  y[1].units[t].position.y}}
			print('attack', client.attack(sA_attack))
			if_gone = 1
			break
		if unit.position.x == y[1].units[t].position.x and unit.position.y == y[1].units[t].position.y - 1:
			sA_attack = {"id" : y[1].units[t].id, "position" : {"x" :  y[1].units[t].position.x, "y" :  y[1].units[t].position.y - 1}}
			print('attack', client.attack(sA_attack))
			if_gone = 1
			break
		if unit.position.x == y[1].units[t].position.x - 1 and unit.position.y == y[1].units[t].position.y:
			sA_attack = {"id" : y[1].units[t].id, "position" : {"x" :  y[1].units[t].position.x - 1, "y" :  y[1].units[t].position.y}}
			print('attack', client.attack(sA_attack))
			if_gone = 1
			break

	s = random.choice([1, 2])
	if if_gone == 0:
		if s == 1:
			sA_move = {"id" : y[1].units[t].id, "position" : {"x" :  y[1].units[t].position.x + 1, "y" :  y[1].units[t].position.y}}
		elif s == 2:
			sA_move = {"id" : y[1].units[t].id, "position" : {"x" :  y[1].units[t].position.x, "y" :  y[1].units[t].position.y - 1}}
		elif s == 3:
			sA_move = {"id" : y[1].units[t].id, "position" : {"x" :  y[1].units[t].position.x - 1, "y" :  y[1].units[t].position.y}}
		elif s == 4:
			sA_move = {"id" : y[1].units[t].id, "position" : {"x" :  y[1].units[t].position.x, "y" :  y[1].units[t].position.y + 1}}
		print('moveUnit', client.moveUnit(sA_move))

	print('wait', client.wait())
	




