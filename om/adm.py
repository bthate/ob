# This file is in the Public Domain.

import threading
import time

from ob.bus import Bus
from ob.prs import elapsed
from ob.obj import Object, edit, fmt, getname

def __dir__():
    return ("flt", "krn", "register", "thr", "upt", "ver")

starttime = time.time()

def flt(clt, event):
    try:
        index = int(event.args[0])
        event.reply(fmt(Bus.objs[index], skip=["queue", "ready", "iqueue"]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))

def krn(clt, event):
    if not event.args:
        event.reply(fmt(k.cfg, skip=["otxt", "opts", "sets", "old", "res"]))
        return
    edit(k.cfg, event.sets)
    k.cfg.save()
    event.reply("ok")

def thr(clt, event):
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        o.update(vars(thr))
        if o.get("sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s(%s)" % (txt, elapsed(up)))
    if res:
        event.reply(" ".join(res))

def upt(clt, event):
    event.reply("uptime is %s" % elapsed(time.time() - starttime))

def ver(clt, event):
    event.reply("%s %s" % (k.cfg.name.upper(), k.cfg.version))
