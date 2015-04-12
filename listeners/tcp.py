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


def thread_main(handler, EventQueue):
    attached = False
    children_lock.acquire()
    try:
        cpipe, ppipe = mp.Pipe()
        self = 'tcp' + str(len(pipes))
    finally:
        children_lock.release()
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
                prc = mp.Process(target=thread_main, args=(self, equeue))
                prc.start()
                prc.join()
        port = 3723
        for s in ARGV:
            if s.startswith('--port='):
                port = int(s[len('--port='):])
        srv = ThreadedTCPServer(('', port), Handler)
        srv.serve_forever()
