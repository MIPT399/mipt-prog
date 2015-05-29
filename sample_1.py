from client import *
import random

print(client.init())
print(client.join("Petya"))
print(client.wait())
print(client.getField())
x = client.getField()
sampleAction = {"id" : x[0].units[0].id, "position" : {"x" : x[0].units[0].position.x + 1, "y" : x[0].units[0].position.y}}
print(client.moveUnit(sampleAction))
print(client.wait())

for i in range(20):
	y = client.getField()
	if_gone = 0
	#print(i, len(y[0].units))
	t = random.randrange(0, len(y[0].units))
	for unit in y[1].units:
		if unit.position.x == y[0].units[t].position.x and unit.position.y == y[0].units[t].position.y + 1:
			sA_attack = {"id" : y[0].units[t].id, "position" : {"x" :  y[0].units[t].position.x, "y" :  y[0].units[t].position.y + 1}}
			print(client.attack(sA_attack))
			if_gone = 1
			break
		if unit.position.x == y[0].units[t].position.x + 1 and unit.position.y == y[0].units[t].position.y:
			sA_attack = {"id" : y[0].units[t].id, "position" : {"x" :  y[0].units[t].position.x + 1, "y" :  y[0].units[t].position.y}}
			print(client.attack(sA_attack))
			if_gone = 1
			break
		if unit.position.x == y[0].units[t].position.x - 1 and unit.position.y == y[0].units[t].position.y:
			sA_attack = {"id" : y[0].units[t].id, "position" : {"x" :  y[0].units[t].position.x - 1, "y" :  y[0].units[t].position.y}}
			print(client.attack(sA_attack))
			if_gone = 1
			break
		if unit.position.x == y[0].units[t].position.x and unit.position.y == y[0].units[t].position.y - 1:
			sA_attack = {"id" : y[0].units[t].id, "position" : {"x" :  y[0].units[t].position.x, "y" :  y[0].units[t].position.y - 1}}
			print(client.attack(sA_attack))
			if_gone = 1
			break
	s = random.randint(1, 4)
	if if_gone == 0:
		if s == 1:
			sA_move = {"id" : y[0].units[t].id, "position" : {"x" :  y[0].units[t].position.x + 1, "y" :  y[0].units[t].position.y}}
		elif s == 2:
			sA_move = {"id" : y[0].units[t].id, "position" : {"x" :  y[0].units[t].position.x - 1, "y" :  y[0].units[t].position.y}}
		elif s == 3:
			sA_move = {"id" : y[0].units[t].id, "position" : {"x" :  y[0].units[t].position.x, "y" :  y[0].units[t].position.y + 1}}
		elif s == 4:
			sA_move = {"id" : y[0].units[t].id, "position" : {"x" :  y[0].units[t].position.x, "y" :  y[0].units[t].position.y - 1}}
		print(client.moveUnit(sA_move))
	print(client.wait())
	




