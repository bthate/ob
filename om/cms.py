# This is file is placed in Public Domain.

def __dir__():
    return ("cmd",)

def cmd(clt, event):
    event.reply(",".join(sorted(k.modules)))
