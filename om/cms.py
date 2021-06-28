# This is file is placed in Public Domain.

import ob

def __dir__():
    return ("cmd",)

def cmd(event):
    k = ob.run.kernel()
    event.reply(",".join(sorted(k.cmds)))
