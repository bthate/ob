# This file is placed in the Public Domain.

from .bus import Bus
from .dpt import Dispatcher
from .err import NotImplemented
from .evt import Command
from .lop import Loop

def __dir__():
    return ('Client',) 

class Client(Dispatcher, Loop):

    def cmd(self, txt):
        Bus.add(self)
        e = self.event(txt)
        e.origin = "root@shell"
        self.dispatch(e)
        e.wait()

    def event(self, txt):
        if txt is None:
            return
        c = Command()
        c.txt = txt or ""
        c.orig = self.__dorepr__()
        return c

    def handle(self, e):
        raise NotImplemented("handle")

    def loop(self):
        while not self.stopped.isSet():
            txt = self.poll()
            if txt is None:
                break
            e = self.event(txt)
            if not e:
                break
            self.handle(e)

    def poll(self):
        return self.queue.get()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        super().start()
        Bus.add(self)