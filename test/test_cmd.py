# This file is placed in the Public Domain.

import random
import unittest

from ob.bus import Bus
from ob.krn import k
from ob.tbl import Table

from prm import param

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(k.cfg.index or 1):
            exec()
        consume()

events = []

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
    l = list(k.modules)
    random.shuffle(l)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd + " " + ex)
            Kernel.dispatch(c, e)
            events.append(e)
