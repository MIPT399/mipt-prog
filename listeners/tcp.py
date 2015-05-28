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


def split(s):
    i = s.find(' ')
    if i == -1:
        return s, ''
    else:
        return s[:i], s[i+1:]

def process_main(handler, EventQueue, self, cpipe):
    attached = False
    name = None
    try:
        while True:
            method, arg = split(handler.rfile.readline().decode().strip())
            if method == 'join':
                name = arg
                EventQueue.put((method, name, self))
                answer = cpipe.recv()
                attached = True
                handler.wfile.write((dumps(answer) + '\n').encode())
                if not answer.result:
                    break
            elif attached and method in {'getField', 'moveUnit', 'attack'}:
                arg = structures.game.load(arg, method)
                if hasattr(arg, 'owner') and getattr(arg, 'owner') != name:
                    handler.wfile.write(b'{"result": false, "cause": "wrong owner"}')
                    continue
                EventQueue.put((method, arg, self))
                answer = cpipe.recv()
                handler.wfile.write((dumps(answer) + '\n').encode())
            else:
                handler.wfile.write('unknown method\n'.encode())
                break 
    finally:
        if name != None:
            EventQueue.put(('disconnect', name, self))


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
                    prc = mp.Process(target=process_main, args=(self, equeue, name, cpipe))
                    children[name] = prc
                finally:
                    children_lock.release()
                prc.start()
                prc.join()
                children_lock.acquire()
                try:
                    if name in status:
                        self.wfile.write(status[name].encode())
                    del status[name]
                    del pipes[name]
                finally:
                    children_lock.release()
        port = 1234
        for s in ARGV:
            if s.startswith('--port='):
                port = int(s[len('--port='):])
        srv = ThreadedTCPServer(('', port), Handler)
        srv.serve_forever()
