# This file is placed in the Public Domain.

import builtins
import getpass
import importlib
import os
import pkgutil
import pwd
import sys
import time

from .bus import Bus
from .clt import Client
from .dft import Default
from .dpt import Dispatcher
from .int import find_cls, find_cmd, find_func
from .lop import Loop
from .obj import Object, cdir, spl
from .prs import parse_txt
from .trm import wrap
from .thr import launch
from .ver import __version__

def __dir__():
    return ('Cfg', 'Kernel')

class Cfg(Default):

    pass

class Kernel(Dispatcher, Loop):

    def __init__(self):
        Dispatcher.__init__(self)
        Loop.__init__(self)
        self.cfg = Cfg()
        self.cmds = Object()
        self.register("cmd", self.dispatch)

    def add(self, func):
        n = func.__name__
        self.cmds[n] = func

    def boot(self, name, wd=None, version=__version__):
        self.parse_cli()
        self.cfg.name = name
        self.cfg.version = version
        self.cfg.update(self.cfg.sets)
        self.cfg.wd = wd or self.cfg.wd or ".ob"
        cdir(self.cfg.wd + os.sep)
        try:
            pwn = pwd.getpwnam(name)
        except KeyError:
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except KeyError:
                return
        try:
            os.chown(self.cfg.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        self.init(self.cfg.m)

    def cmd(self, clt, txt):
        Bus.add(clt)
        e = clt.event(txt)
        e.origin = "root@shell"
        self.dispatch(e)
        e.wait()

    def do(self, e):
        self.dispatch(e)

    def error(self, e):
        pass

    def handle(self, hdl, obj):
        obj.parse()
        f = self.cmds.get(obj.cmd, None)
        if f:
            f(obj)
            obj.show()
        obj.ready()

    def init(self, mns):
        for mn in spl(mns):
            mod = sys.modules.get(mn, None)
            if mod and "init" in dir(mod):
                launch(mod.init, self)

    def opts(self, ops):
        for opt in ops:
            if opt in self.cfg.opts:
                return True
        return False

    def parse_cli(self):
        txt = " ".join(sys.argv[1:])
        o = Default()
        parse_txt(o, txt)
        self.cfg.update(o)

    @staticmethod
    def privileges(name=None):
        if os.getuid() != 0:
            return
        if name is None:
            try:
                name = getpass.getuser()
            except KeyError:
                pass
        try:
            pwnam = pwd.getpwnam(name)
        except KeyError:
            return False
        os.setgroups([])
        os.setgid(pwnam.pw_gid)
        os.setuid(pwnam.pw_uid)
        old_umask = os.umask(0o22)
        return True

    @staticmethod
    def root():
        if os.geteuid() != 0:
            return False
        return True

    def scan(self, pkgs=""):
        res = {}
        for pn in spl(pkgs):
            p = sys.modules.get(pn, None)
            if not p:
                continue
            for mn in pkgutil.walk_packages(p.__path__, pn+"."):
                zip = mn[0].find_module(mn[1])
                mod = zip.load_module(mn[1])
                self.introspect(mod)
                
    def start(self):
        super().start()
        self.parse_cli()
        self.register("cmd", self.handle)

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)

def kernel():
    return getattr(sys.modules["__main__"], "k", None)
