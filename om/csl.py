# This file is placed in the Public Domain.

from ob.clt import Client
from ob.thr import launch

def init(k):
    c = Console()
    c.start()
    return c

class CLI(Client):

    def error(self, e):
        print(e.exc)
        raise Restart

    def raw(self, txt):
        print(txt)

class Console(CLI):

    def handle(self, e):
        super().handle(e)
        e.wait()

    def poll(self):
        return input("> ")
