# This file is placed in the Public Domain.

import atexit
import builtins
import getpass
import importlib
import inspect
import ob
import os
import pkgutil
import pwd
import queue
import sys
import termios
import threading
import time
import types

def __dir__():
    return ('Cfg', 'Kernel', 'Repeater', 'Timer', 'wrap')

resume = {}

class Restart(Exception):

    pass

class Cfg(ob.Default):

    pass

class Kernel(ob.hdl.Dispatcher, ob.hdl.Loop):

    def __init__(self):
        ob.hdl.Dispatcher.__init__(self)
        ob.hdl.Loop.__init__(self)
        self.cfg = Cfg()
        self.cmds = ob.Object()
        self.register("cmd", self.handle)

    def add(self, func):
        n = func.__name__
        self.cmds[n] = func

    def boot(self, wd=""):
        self.parse_cli(wd)
        ob.cdir(self.cfg.wd + os.sep)
        self.scan(self.cfg.p)
        self.init(self.cfg.m)

    def cmd(self, clt, txt):
        ob.hdl.Bus.add(clt)
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
        for mn in ob.spl(mns):
            mod = sys.modules.get(mn, None)
            i = getattr(mod, "init", None)
            if i:
                ob.launch(i, self)

    def introspect(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1 and "event" in o.__code__.co_varnames:
                self.cmds[o.__name__] = o

    def opts(self, ops):
        for opt in ops:
            if opt in self.cfg.opts:
                return True
        return False

    def parse_cli(self, wd=""):
        txt = " ".join(sys.argv[1:])
        o = ob.Default()
        ob.prs.parse_txt(o, txt)
        self.cfg.update(o)
        self.cfg.update(self.cfg.sets)
        ob.wd = ob.wd or self.cfg.wd or wd or None

    @staticmethod
    def privileges(name=None):
        if os.getuid() != 0:
            return
        try:
            pwn = pwd.getpwnam(name)
        except KeyError:
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except KeyError:
                return
        if name is None:
            try:
                name = getpass.getuser()
            except KeyError:
                pass
        try:
            pwn = pwd.getpwnam(name)
        except KeyError:
            return False
        try:
            os.chown(ob.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
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
        for pn in ob.spl(pkgs):
            p = sys.modules.get(pn, None)
            if not p:
                try:
                    p = __import__(pn)
                except ModuleNotFoundError:
                    continue
            for mn in pkgutil.walk_packages(p.__path__, pn+"."):
                zip = mn[0].find_module(mn[1])
                mod = zip.load_module(mn[1])
                self.introspect(mod)
                
    def start(self, wd=""):
        self.boot(wd)
        super().start()

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)

class Timer(ob.Object):

    def __init__(self, sleep, func, *args, name=None):
        super().__init__()
        self.args = args
        self.func = func
        self.sleep = sleep
        self.name = name or  ""
        self.state = ob.Object()
        self.timer = None

    def run(self):
        self.state.latest = time.time()
        ob.launch(self.func, *self.args)

    def start(self):
        if not self.name:
            self.name = ob.getname(self.func)
        timer = threading.Timer(self.sleep, self.run)
        timer.setName(self.name)
        timer.setDaemon(True)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def stop(self):
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    def run(self):
        thr = ob.launch(self.start)
        super().run()
        return thr

def kernel():
    return getattr(sys.modules["__main__"], "k", None)

def termsetup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        try:
            termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])
        except termios.error:
            pass

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = termsetup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass

def wrap(func):
    termsave()
    try:
        func()
    except KeyboardInterrupt:
        pass
    finally:
        termreset()
