# This file is placed in the Public Domain.

import random
import sys
import unittest

from ob.bus import Bus
from ob.krn import k
from ob.thr import launch

from prm import param

class Test_Threaded(unittest.TestCase):

    def setUp(self):
        k.cfg.wd = ".test"

    def test_thrs(self):
        thrs = []
        for x in range(k.cfg.index or 1):
            thr = launch(exec)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
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
            e = c.event(cmd+" "+ex)
            k.put(e)
            events.append(e)
