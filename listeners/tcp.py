import socketserver
from logic.main import ARGV
from json import dumps
import multiprocessing as mp
from listeners.main import *
import socket
import structures.game

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


def threadMain(handler, EventQueue):
    def processMain(handler, name, cpipe, self):
        while True:
            method = handler.rfile.readline().decode().strip()
            arg = handler.rfile.readline().decode().strip()
            if method in {'getField', 'moveUnit', 'attack'}:
                EventQueue.put((method, structures.game.load(arg, method), self))
                answer = cpipe.recv()
                handler.wfile.write((dumps(answer) + '\n').encode())
            else:
                handler.wfile.write('unknown method\n'.encode())
                break
    method = handler.rfile.readline().decode().strip()
    arg = handler.rfile.readline().decode().strip()
    if method == 'join':
        name = arg
        children_lock.acquire()
        try:
            cpipe, ppipe = mp.Pipe()
            if ('tcp'+name) not in pipes:
                pipes['tcp'+name] = ppipe
                prc = mp.Process(target=processMain, args=(handler, name, cpipe, 'tcp'+name))
                prc.start()
                return prc
        finally:
            children_lock.release()
    print("I don't know you.\n".encode())


@listener('TCP')
class GameListener:
    def __init__(self, EventQueue):
        self.EventQueue = EventQueue
    def main(self):
        equeue = self.EventQueue
        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                threadMain(self, equeue).join()
        port = 3721
        for s in ARGV:
            if s.startswith('--port='):
                port = int(s[len('--port='):])
        srv = ThreadedTCPServer(('', port), Handler)
        srv.serve_forever()
