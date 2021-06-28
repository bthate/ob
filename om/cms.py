# This is file is placed in Public Domain.

from run import kernel

def __dir__():
    return ("cmd",)

def cmd(event):
    k = kernel()
    event.reply(",".join(sorted(k.cmds)))
