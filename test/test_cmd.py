# This file is placed in the Public Domain.

import ob
import time
import unittest

from prm import consume, events, exec, k, param, times

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(k.cfg.index or 1):
            times[x] = ob.Object()
            times[x].start = time.time()
            exec()
            times[x].stop = time.time()
        consume()
