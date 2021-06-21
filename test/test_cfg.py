# This file is placed in the Public Domain.

import unittest

from ob.dft import Default
from ob.obj import edit
from ob.prs import parse_txt

cfg = Default()

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        parse_txt(cfg, "mods=irc")
        self.assertEqual(cfg.sets.mods, "irc")

    def test_parse2(self):
        parse_txt(cfg, "mods=irc,udp")
        self.assertEqual(cfg.sets.mods, "irc,udp")

    def test_edit(self):
        d = {"mods": "rss"}
        edit(cfg, d)
        self.assertEqual(cfg.mods, "rss")
