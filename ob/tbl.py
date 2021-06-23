# This file is placed in the Public Domain.

import builtins
import inspect
import importlib
import os
import sys

from .dft import Default
from .err import NoClass
from .obj import Object

def __dir__():
    return ('Table', "builtin")

reserved = ["cdir", "wrap"]

class Table(Object):

    classes = Object()
    cmds = Object()
    fulls = Object()
    names = Default()
    modules = Object()
    table = Object()

    @staticmethod
    def addcmd(func):
        n = func.__name__
        Table.modules[n] = func.__module__
        Table.cmds[n] = func

    @staticmethod
    def addcls(clz):
        nn = "%s.%s" % (clz.__module__, clz.__name__)
        if nn in Table.classes:
            return
        n = clz.__name__.lower()
        if n not in Table.names:
            Table.names[n] = []
        if n not in Table.names[n]:
            Table.names[n].append(nn)
        Table.classes[nn] = clz

    @staticmethod
    def addmod(mod):
        n = mod.__spec__.name
        Table.fulls[n.split(".")[-1]] = n
        Table.table[n] = mod

    @staticmethod
    def getcls(name):
        return Table.classes.get(name, None)

    @staticmethod
    def getcmd(c):
        return Table.cmds.get(c, None)

    @staticmethod
    def getfull(c):
        return Table.fulls.get(c, None)

    @staticmethod
    def getmod(mn):
        return Table.table.get(mn, None)

    @staticmethod
    def getnames(nm, dft=None):
        return Table.names.get(nm, dft)

    @staticmethod
    def getmodule(mn, dft):
        return Table.modules.get(mn, dft)

    @staticmethod
    def register(mod):
        Table.addmod(mod)
        classes = find_cls(mod)
        for nm, c in classes.items():
            Table.addcls(c)
        commands = find_cmd(mod)
        for nm, c in commands.items():
            Table.addcmd(c)

    @staticmethod
    def mod(m):
        Table.addmod(m)
        classes = find_cls(m)
        for nm, c in classes.items():
            built(nm, c)
        commands = find_cmd(m)
        for nm, c in commands.items():
            built(nm, c)
        functions = find_func(m)
        for nm, f in functions.items():
            built(nm, f)

def builtin(nm, o):
    setattr(builtins, nm, o)

def find_cls(mod):
    res = {}
    pn = mod.__package__
    for key, o in inspect.getmembers(mod, inspect.isclass):
        n = "%s.%s.%s" % (pn, o.__module__, o.__name__)
        res[n] = o
    return res

def find_cmd(mod):
    res = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if o.__code__.co_argcount == 1 and "event" in o.__code__.co_varnames:
            res[o.__name__] = o
    return res

def find_func(mod):
    res = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if key in reserved:
            if "event" not in o.__code__.co_varnames:
                res[o.__name__] = o
    return res
