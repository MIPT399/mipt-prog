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


def process_main(handler, EventQueue, self, cpipe):
    attached = False
    while True:
        method = handler.rfile.readline().decode().strip()
        arg = handler.rfile.readline().decode().strip()
        if method == 'join':
            EventQueue.put((method, arg, self))
            answer = cpipe.recv()
            if not answer.result:
                break
            attached = True
            handler.wfile.write((dumps(answer) + '\n').encode())
        elif attached and method in {'getField', 'moveUnit', 'attack'}:
            EventQueue.put((method, structures.game.load(arg, method), self))
            answer = cpipe.recv()
            handler.wfile.write((dumps(answer) + '\n').encode())
        else:
            handler.wfile.write('unknown method\n'.encode())
            break
    print("Go away!\n".encode())


@listener('TCP')
class GameListener:
    def __init__(self, EventQueue):
        self.EventQueue = EventQueue
    def main(self):
        equeue = self.EventQueue
        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                children_lock.acquire()
                try:
                    cpipe, ppipe = mp.Pipe()
                    name = 'tcp' + str(len(pipes))
                    pipes[name] = ppipe
                finally:
                    children_lock.release()
                prc = mp.Process(target=process_main, args=(self, equeue, name, cpipe))
                prc.start()
                prc.join()
        port = 3721
        for s in ARGV:
            if s.startswith('--port='):
                port = int(s[len('--port='):])
        srv = ThreadedTCPServer(('', port), Handler)
        srv.serve_forever()
