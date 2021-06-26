# This file is placed in the Public Domain.

import queue
import threading

from .lst import List
from .obj import Object
from .thr import launch

class Output(Object):

    def __init__(self):
        Object.__init__(self)
        self.cache = List()
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()
        
    @staticmethod
    def append(channel, txtlist):
        if channel not in Output.cache:
            self.cache[channel] = []
        self.cache[channel].extend(txtlist)

    def dosay(self, channel, txt):
        pass

    def oput(self, channel, txt):
        self.oqueue.put_nowait((channel, txt))

    def output(self):
        while not self.dostop.isSet():
            (channel, txt) = self.oqueue.get()
            if self.dostop.isSet() or channel is None:
                break
            self.dosay(channel, txt)

    @staticmethod
    def size(name):
        if name in self.cache:
            return len(self.cache[name])
        return 0

    def start(self):
        self.dostop.clear()
        launch(self.output)
        return self

    def stop(self):
        self.dostop.set()
        self.oqueue.put_nowait((None, None))
