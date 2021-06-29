# This file is placed in the Public Domain.

import ob
import unittest

from ob import Default, parse_txt

cfg = Default()

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        parse_txt(cfg, 'm=om.irc')
        self.assertEqual(cfg.sets.m, 'om.irc')

    def test_parse2(self):
        parse_txt(cfg, 'm=om.irc,om.udp,om.rss')
        self.assertEqual(cfg.sets.m,'om.irc,om.udp,om.rss')

    def test_edit(self):
        d = {'m':'om.rss'}
        cfg.edit(d)
        self.assertEqual(cfg.m, "om.rss")
