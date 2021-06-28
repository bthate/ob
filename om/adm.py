# This file is in the Public Domain.

import ob
import threading
import time

def __dir__():
    return ("flt", "krn", "register", "thr", "upt", "ver")

k = ob.run.kernel()
starttime = time.time()

def flt(event):
    try:
        index = int(event.args[0])
        event.reply(ob.fmt(ob.hdl.Bus.objs[index], skip=["queue", "ready", "iqueue"]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([ob.getname(o) for o in ob.hdl.Bus.objs]))

def krn(event):
    k = kernel()
    if not event.args:
        event.reply(ob.fmt(k.cfg, skip=["otxt", "opts", "sets", "old", "res"]))
        return
    k.cfg.edit(event.sets)
    k.cfg.save()
    event.reply("ok")

def thr(event):
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = ob.Object()
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
        res.append("%s(%s)" % (txt, ob.prs.elapsed(up)))
    if res:
        event.reply(" ".join(res))

def upt(event):
    event.reply("uptime is %s" % elapsed(time.time() - starttime))
