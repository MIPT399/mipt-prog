__author__ = 'arterm'

from client import *
import random
import math

name = str(random.randint(10000000, 12345689))

print(client.init())
print(client.join(name))
print(client.wait())


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def dist(a, b):
    return math.fabs(a.x - b.x) + math.fabs(a.y - b.y)

def cook(id, x, y):
    return {"id": id, "position": {"x": x, "y": y}}

dirs = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]


while True:
    field = client.getField()
    for x in field:
        if x.name == name:
            global me
            me = x

    if me.units == []:
        print(client.wait())
        continue

    cur = random.choice(me.units)
    pos = Point(cur.position.x, cur.position.y)
    used = False

    best_to = dirs[0]
    best_dist = 100000

    for to in dirs:
        for pl in field:
            if pl.name != name:
                for u in pl.units:
                    u_pos = Point(u.position.x, u.position.y)
                    if dist(pos + to, u_pos) < best_dist:
                        best_dist = dist(pos + to, u_pos)
                        best_to = to
                    if pos + to == u_pos and not used:
                        query = cook(cur.id, u_pos.x, u_pos.y)
                        print(client.attack(query))
                        used = True

    if not used:
        to = pos + best_to
        query = cook(cur.id, to.x, to.y)
        print(client.moveUnit(query))

    print(client.wait())





