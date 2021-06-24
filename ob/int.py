# This file is placed in the Public Domain.

import builtins
import inspect

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
