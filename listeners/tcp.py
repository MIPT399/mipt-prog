from socketserver import TCPServer, BaseRequestHandler
from logic.main import ARGV
from json import loads, dumps
import threading
import multiprocessing as mp
from listeners.main import children_lock

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def threadMain(handler, EventQueue):
    def processMain(handler, name, cpipe, self):
        while True:
            s = handler.rfile.readline()
            method, arg = split(s, ':')
            if method in {'getField', 'moveUnit', 'attack'}:
                EventQueue.put((method, arg, self))
                answer = cpipe.recv()
                handler.wfile.write(dumps(answer) + '\n')
            else:
                handler.wfile.write('unknown method\n')
    while True:
        s = handler.rfile.readline()
        method, arg = split(s, ':')
        name = None
        if method == 'join':
            children_lock.acquire()
            cpipe, ppipe = mp.Pipe()
            if ('tcp'+name) not in pipes:
                pipes['tcp'+name] = ppipe
                mp.Process(target=processMain, args=(handler, name, cpipe, 'tcp'+name)).start()
            children_lock.release()
            return
        else:
           print("I don't know you.\n")
    
@listener('TCP')
class GameListener:
    def __init__(self, EventQueue):
        self.EventQueue = EventQueue
    
    def main(self):
        equeue = self.EventQueue
        class Handler(BaseRequestHandler):
            def handle(self):
                threading.Thread(target=threadMain, args=(self, equeue))
                threadMain(selfa)
        port = 3721
        for s in  ARGV:
            if s.startswith('--port='):
                port = int(s[len('--port='):])
        srv = ThreadedTCPServer(('', port), Handler)
        srv.serve_forever()
