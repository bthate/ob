# This file is placed in the Public Domain.

from .bus import Bus
from .err import Restart, Stop
from .evt import Command, Event
from .obj import Object
from .thr import launch
from .trc import get_exception

import queue
import threading

class Handler(Object):

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.queue = queue.Queue()
        self.speed = "normal"
        self.stopped = threading.Event()

    def callbacks(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def error(self, event):
        pass

    def event(self, txt):
        c = Command()
        c.txt = txt or ""
        c.orig = self.__dorepr__()
        return c

    def handle(selfe):
        self.queue.put(e)

    def dispatcher(self):
        dorestart = False
        self.stopped.clear()
        while not self.stopped.isSet():
            e = self.queue.get()
            try:
                self.callbacks(e)
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

    def register(self, name, callback):
        self.cbs[name] = callback

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        self.register("cmd", k.dispatch)
        launch(self.dispatcher)
        return self

    def stop(self):
        self.stopped.set()
        self.queue.put(None)
