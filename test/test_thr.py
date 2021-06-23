# This file is placed in the Public Domain.

import random
import sys
import unittest

from ob.bus import Bus
from ob.evt import Command
from ob.obj import cfg
from ob.tbl import Table
from ob.thr import launch
from ob.krn import Kernel

from prm import param

class Test_Threaded(unittest.TestCase):

    def setUp(self):
        cfg.wd = ".test"
        k.stop()
        k.start()
        
    def TearDown(self):
        k.stop()
 
    def test_thrs(self):
        thrs = []
        for x in range(Kernel.cfg.index or 1):
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
    l = list(Table.modules)
    random.shuffle(l)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd+" "+ex)
            C.handle(e)
            events.append(e)
