from client import *

"""for name in ["abc", "cde", "Surin", "Golov", "Arterm"]:
	client.init()
	client.join(name)
	client.getField()
	client.close()
"""

print(client.init())
print(client.join("Vasya"))
print(client.getField())
sampleAction = {"owner" : "Vasya", "id" : "123", "position" : {"x" : 0, "y" : 1234}}
print(client.moveUnit(sampleAction))
print(client.attack(sampleAction))
print(client.close())