# This is file is placed in Public Domain.

from .tbl import Table

def __dir__():
    return ("cmd",)

def cmd(event):
    event.reply(",".join(sorted(Table.modules)))
