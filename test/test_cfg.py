# This file is placed in the Public Domain.

import ob
import unittest

from ob import Default
from ob.prs import parse_txt

cfg = ob.Default()

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        ob.prs.parse_txt(cfg, "mods=irc")
        self.assertEqual(cfg.sets.mods, "irc")

    def test_parse2(self):
        ob.prs.parse_txt(cfg, "mods=irc,udp")
        self.assertEqual(cfg.sets.mods, "irc,udp")

    def test_edit(self):
        d = {"mods": "rss"}
        cfg.edit(d)
        self.assertEqual(cfg.mods, "rss")
