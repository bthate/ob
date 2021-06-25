# This file is placed in the Public Domain.

import builtins
import inspect
import importlib
import os
import sys

from .dft import Default
from .err import NoClass
from .int import find_cls, find_cmd, find_func
from .obj import Object

def __dir__():
    return ('Table',)

class Table(Object):

    def __init__(self):
        super().__init__()
        self.classes = Object()
        self.cmds = Object()
        self.fulls = Object()
        self.names = Default()
        self.modules = Object()
        self.table = Object()

    def addcmd(self, func):
        n = func.__name__
        self.modules[n] = func.__module__
        self.cmds[n] = func

    def addcls(self, clz):
        nn = "%s.%s" % (clz.__module__, clz.__name__)
        if nn in self.classes:
            return
        n = clz.__name__.lower()
        if n not in self.names:
            self.names[n] = []
        if n not in self.names[n]:
            self.names[n].append(nn)
        self.classes[nn] = clz

    def addmod(self, mod):
        n = mod.__spec__.name
        self.fulls[n.split(".")[-1]] = n
        self.table[n] = mod

    def getcls(self, name):
        return self.classes.get(name, None)

    def getcmd(self, c):
        return self.cmds.get(c, None)

    def getfull(self, c):
        return self.fulls.get(c, None)

    def getmod(self, mn):
        return self.table.get(mn, None)

    def getnames(self, nm, dft=None):
        return self.names.get(nm, dft)

    def getmodule(self, mn, dft):
        return self.modules.get(mn, dft)

    def introspect(self, mod):
        self.addmod(mod)
        classes = find_cls(mod)
        for nm, c in classes.items():
            self.addcls(c)
        commands = find_cmd(mod)
        for nm, c in commands.items():
            self.addcmd(c)

    def reserved(self, m):
        self.addmod(m)
        classes = find_cls(m)
        for nm, c in classes.items():
            builtin(nm, c)
        commands = find_cmd(m)
        for nm, c in commands.items():
            builtin(nm, c)
        functions = find_func(m)
        for nm, f in functions.items():
            builtin(nm, f)

def builtin(nm, o):
    setattr(builtins, nm, o)
