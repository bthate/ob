# This file is placed in the Public Domain.

import random

from ob.bus import Bus
from ob.krn import k
from ob.obj import Object

events = []

param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["cfg server=localhost", "cfg", ""]
param.dne = ["test4", ""]
param.rm = ["reddit", ""]
param.dpl = ["reddit title,summary,link", ""]
param.log = ["test1", ""]
param.flt = ["0", "1", ""]
param.fnd = ["cfg",
             "log",
             "todo",
             "rss",
             "irc server==localhost",
             "rss rss==reddit rss"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]
#param.mbx = ["~/Desktop/25-1-2013", ""]

def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res

def exec():
    c = Bus.first()
    print(str(type(c)))
    l = list(k.modules)
    random.shuffle(l)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd + " " + ex)
            k.dispatch(c, e)
            events.append(e)
