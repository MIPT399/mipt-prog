import socket
import json
import sys

__all__ = ["method", "getField", "stop", "close", "init", "stop", "moveUnit", "attack"]

HOST, PORT = "localhost", 1234

def init():
	global sock
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
	return json.loads(send("join " + name))

def method():
	send("join Hu23")

def getField():
	return json.loads(send("getField"))

def moveUnit(action):
	return json.loads(send("moveUnit " + json.dumps(action)))

def attack(action):
	return json.loads(send("attack " + json.dumps(action)))

def close():
	sock.close()

def stop():
	return send("stop")
