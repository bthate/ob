# This is file is placed in Public Domain.

from ob.krn import k

def __dir__():
    return ("cmd",)

def cmd(event):
    event.reply(",".join(sorted(k.modules)))
