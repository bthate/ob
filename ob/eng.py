# This file is placed in the Public Domain.

from .dpt import Dispatcher

def __dir__():
    return ('Engine',)

class Engine(Dispatcher):

    def __init__(self):
        super().__init__()
        self.cbs = Object()

    def dispatch(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def register(self, name, callback):
        self.cbs[name] = callback
