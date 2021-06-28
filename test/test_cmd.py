# This file is placed in the Public Domain.

import ob
import unittest

events = []
k = ob.run.kernel()

param = ob.Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["cfg server=localhost", "cfg", ""]
param.dne = ["test4", ""]
param.rm = ["reddit", ""]
param.dpl = ["reddit title,summary,link", ""]
param.log = ["test1", ""]
param.flt = ["0", ""]
param.fnd = ["om.irc.Cfg",
             "om.log.Log",
             "om.tdo.Todo",
             "om.rss.Rss",
             "om.irc.Cfg server==localhost",
             "om.rss.Rss rss==reddit rss"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]

class Test_Commands(unittest.TestCase):

    def test_commands(self):
        c = ob.hdl.Bus.first()
        l = list(k.cmds)
        for cmd in l:
            for ex in getattr(param, cmd, [""]):
                e = c.event(cmd + " " + ex)
                k.dispatch(e)
                events.append(e)
