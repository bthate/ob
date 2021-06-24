# This file is in the Public Domain.

from ob.dbs import find
from ob.obj import Object

def __dir__():
    return ("Todo", "dne", "tdo")

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def dne(clt, event):
    if not event.args:
        event.reply("dne txt==<string>")
        return
    for fn, o in find("todo", event.gets):
        o._deleted = True
        o.save()
        event.reply("ok")
        break

def tdo(clt, event):
    if not event.rest:
        event.reply("tdo <txt>")
        return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")
