# This file is placed in the Public Domain.

import queue
import threading

from .bus import Bus
from .evt import Command
from .krn import kernel
from .obj import Object
from .thr import launch

class Client(Object):

    def __init__(self):
        super().__init__()
        self.iqueue = queue.Queue()
        self.speed = "normal"
        self.stopped = threading.Event()
        self.target = None

    def event(self, txt):
        if txt is None:
            return
        c = Command()
        c.txt = txt or ""
        c.orig = self.__dorepr__()
        return c

    def handle(self, clt, e):
        self.target.put(clt, e)

    def handler(self):
        while not self.stopped.isSet():
            txt = self.poll()
            if txt is None:
                break
            e = self.event(txt)
            if not e:
                break
            self.handle(self, e)

    def poll(self):
        return self.iqueue.get()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)

    def put(self, e):
        self.iqueue.put_nowait(e)

    def start(self):
        self.target = k
        Bus.add(self)
        launch(self.handler)
        return self

    def stop(self):
        self.stopped.set()
        self.iqueue.put(None)
