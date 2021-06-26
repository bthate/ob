# This file is placed in the Public Domain.

import unittest

from ob.krn import k

from prm import param, consume, events, exec

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(k.cfg.index or 1):
            exec()
        consume()
