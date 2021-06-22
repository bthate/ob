# This file is placed in the Public Domain.

import getpass
import importlib
import ob
import os
import pkgutil
import pwd
import sys
import time

from .dft import Default
from .obj import Object, cdir, cfg, spl
from .prs import parse_txt
from .hdl import Handler
from .tbl import Table
from .trm import wrap
from .thr import launch
from .ver import __version__

def __dir__():
    return ('Cfg', 'Kernel', "Table", "cfg", "os", "sys", "wrap")

class Cfg(Default):

    pass

class Kernel(Handler):

    cfg = Cfg()
    table = Object()
 
    @staticmethod
    def boot(name, version=__version__):
        Kernel.parse()
        Kernel.cfg.name = name
        Kernel.cfg.version = version
        Kernel.cfg.update(Kernel.cfg.sets)
        Kernel.cfg.wd = cfg.wd = Kernel.cfg.wd or cfg.wd
        cdir(Kernel.cfg.wd + os.sep)
        try:
            pwn = pwd.getpwnam(name)
        except KeyError:
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except KeyError:
                return
        try:
            os.chown(Kernel.cfg.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        Kernel.privileges()
        Kernel.scan(Kernel.cfg.pkgs)
        Kernel.init(Kernel.cfg.mods)

    @staticmethod
    def init(mns):
        for mn in spl(mns):
            mnn = Table.getfull(mn)
            mod = Table.getmod(mnn)
            if "init" in dir(mod):
                launch(mod.init, Kernel)

    @staticmethod
    def opts(ops):
        for opt in ops:
            if opt in Kernel.cfg.opts:
                return True
        return False

    @staticmethod
    def parse():
        txt = " ".join(sys.argv[1:])
        o = Object()
        parse_txt(o, txt)
        Kernel.cfg.update(o)

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

    @staticmethod
    def scan(pkgs):
        for pn in spl(pkgs):
            try:
                mod = __import__(pn)
            except ModuleNotFoundError:
                return
            for mn in pkgutil.walk_packages(mod.__path__, pn+"."):
                if mn[1] == "%s.%s.tbl" % (pn, mn[1]):
                    continue
                zip = mn[0].find_module(mn[1])
                mod = zip.load_module(mn[1])
                Table.register(mod)

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)

def getdir(mod):
    return mod.__path__[0]
