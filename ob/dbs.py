# This file is placed in the Public Domain.

from .err import NoType
from .krn import k
from .obj import gettype

import os
import sys
import time

def __dir__():
    return ('all', 'deleted', 'every', 'find', 'last', 'lasttype', 'lastfn', 'fntime', 'hook')

def all(otype, selector=None, index=None, timed=None):
    nr = -1
    if selector is None:
        selector = {}
    otypes = k.getnames(otype, [])
    for t in otypes:
        for fn in fns(t, timed):
            o = hook(fn)
            if selector and not o.search(selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

def deleted(otype):
    otypes = k.getnames(otype, [])
    for t in otypes:
        for fn in fns(t):
            o = hook(fn)
            if "_deleted" not in o or not o._deleted:
                continue
            yield fn, o

def every(selector=None, index=None, timed=None):
    if selector is None:
        selector = {}
    nr = -1
    for otype in os.listdir(os.path.join(k.cfg.wd, "store")):
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not o.search(selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

def find(otypes, selector=None, index=None, timed=None):
    if selector is None:
        selector = {}
    got = False
    nr = -1
    for t in otypes:
        for fn in fns(t, timed):
            o = hook(fn)
            if selector and not o.search(selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            got = True
            yield (fn, o)
    if not got:
        return (None, None)

def last(o):
    t = str(gettype(o))
    path, l = lastfn(t)
    if  l:
        o.update(l)
    if path:
        spl = path.split(os.sep)
        stp = os.sep.join(spl[-4:])
        return stp

def lastmatch(otype, selector=None, index=None, timed=None):
    res = sorted(find(otype, selector, index, timed), key=lambda x: fntime(x[0]))
    if res:
        return res[-1]
    return (None, None)

def lasttype(otype):
    fnn = fns(otype)
    if fnn:
        return hook(fnn[-1])

def lastfn(otype):
    fn = fns(otype)
    if fn:
        fnn = fn[-1]
        return (fnn, hook(fnn))
    return (None, None)

def fns(name, timed=None):
    if not name:
        return []
    p = os.path.join(k.cfg.wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if timed and "from" in timed and timed["from"] and fntime(p) < timed["from"]:
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)

def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        t += float("." + rest)
    else:
        t = 0
    return t

def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    mn, cn = cname.rsplit(".", 1)
    mod = sys.modules.get(mn)
    t = getattr(mod, cn, None)
    #t = k.classes.get(cname, None)
    #if not t:
    #    raise NoType(cname)
    if fn:
        o = t()
        o.load(fn)
        return o
    raise NoType(cname)

def listfiles(wd):
    path = os.path.join(wd, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))
