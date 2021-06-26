# This file is placed in the Public Domain.

import unittest

from ob.krn import k
from ob.thr import launch

from prm import param, consume, events, exec

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

