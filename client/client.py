import socket
import json
import sys
from structures.game import AttrDict 

__all__ = ["method", "getField", "stop", "close", "init", "stop", "moveUnit", "attack", "join", "wait"]

NAME, HOST, PORT = "", "localhost", 1234

def parse(source):
    return json.loads(source, object_hook=AttrDict)

def init(host="localhost", port=1234):
        global sock
        global HOST
        global PORT
        HOST, PORT = host, port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

def send(data):
        try:
                sock.sendall(bytes(data + "\n", "utf-8"))
                #print("sent {}".format(data))
                received = str(sock.recv(1024), "utf-8")
                return received
        except:
                print("Something really bad has happened", file = sys.stderr)

def join(name):
        global NAME
        NAME = name
        return parse(send("join " + name))

def method():
        send("join Hu23")

def getField():
        return parse(send("getField"))

def moveUnit(action):
        action['owner'] = NAME
        return parse(send("moveUnit " + json.dumps(action)))

def attack(action):
        action['owner'] = NAME
        return parse(send("attack " + json.dumps(action)))

def close():
        sock.close()

def stop():
        return send("stop")

def wait():
	return send("wait")

