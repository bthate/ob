# This file is placed in the Public Domain.

import queue
import threading

from .err import NotImplemented
from .evt import Event
from .obj import Object
from .thr import launch
from .trc import get_exception

class Dispatcher(Object):

    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.stopped = threading.Event()

    def dispatch(self, e):
        raise NotImplemented        
        
    def error(self, e):
        raise NotImplemented        

    def dispatcher(self):
        dorestart = False
        self.stopped.clear()
        while not self.stopped.isSet():
            e = self.queue.get()
            try:
                self.dispatch(e)
            except Restart:
                dorestart = True
                break
            except Stop:
                break
            except Exception as ex:
                e = Event()
                e.type = "error"
                e.exc = get_exception()
                self.error(e)
        if dorestart:
            self.restart()

    def restart(self):
        self.stop()
        self.start()

    def put(self, e):
        self.queue.put_nowait(e)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        launch(self.dispatcher)
        return self

    def stop(self):
        self.stopped.set()
        self.queue.put(None)
