# This file is placed in the Public Domain.

import ob
import queue
import sys
import threading

from prs import parse_txt

def __dir__():
    return ('Bus', 'Command', 'Dispatcher', 'Event', 'Handler', 'Loop', 'NoBot', 'NotImplemented', 'Restart', 'Stop') 

class NotImplemented(Exception):

    pass

class Restart(Exception):

    pass

class Stop(Exception):

    pass

class NoBot(Exception):

    pass

class Bus(ob.Object):

    objs = []

    def __iter__(self):
        return iter(Bus.objs)

    @staticmethod
    def add(obj):
        if obj not in Bus.objs:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        for h in Bus.objs:
            if "announce" in dir(h):
                h.announce(txt)

    @staticmethod
    def byorig(orig):
        for o in Bus.objs:
            if o.__dorepr__() == orig:
                return o

    @staticmethod
    def byfd(fd):
        for o in Bus.objs:
            if o.fd and o.fd == fd:
                return o

    @staticmethod
    def bytype(typ):
        for o in Bus.objs:
            if isinstance(o, type):
                return o

    def first(otype=None):
        if Bus.objs:
            if not otype:
                return Bus.objs[0]
            for o in Bus.objs:
                if otype in str(type(o)):
                    return o

    @staticmethod
    def resume():
        for o in Bus.objs:
            o.resume()

    @staticmethod
    def say(orig, channel, txt):
        for o in Bus.objs:
            if o.__dorepr__() == orig:
                o.say(channel, txt)

class Dispatcher(ob.Object):

    def __init__(self):
        super().__init__()
        self.cbs = ob.Object()

    def dispatch(self, event):
        if event and event.type in self.cbs:
            self.cbs[event.type](self, event)
        else:
            event.ready()

    def register(self, name, callback):
        self.cbs[name] = callback

class Output(ob.Object):

    def __init__(self):
        ob.Object.__init__(self)
        self.cache = ob.List()
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()
        
    @staticmethod
    def append(channel, txtlist):
        if channel not in Output.cache:
            self.cache[channel] = []
        self.cache[channel].extend(txtlist)

    def dosay(self, channel, txt):
        pass

    def oput(self, channel, txt):
        self.oqueue.put_nowait((channel, txt))

    def output(self):
        while not self.dostop.isSet():
            (channel, txt) = self.oqueue.get()
            if self.dostop.isSet() or channel is None:
                break
            self.dosay(channel, txt)

    @staticmethod
    def size(name):
        if name in self.cache:
            return len(self.cache[name])
        return 0

    def start(self):
        self.dostop.clear()
        ob.launch(self.output)
        return self

    def stop(self):
        self.dostop.set()
        self.oqueue.put_nowait((None, None))

class Event(ob.Default):

    def __init__(self):
        super().__init__()
        self.channel = None
        self.done = threading.Event()
        self.error = ""
        self.exc = None
        self.orig = None
        self.result = []
        self.thrs = []
        self.type = "event"
        self.txt = None

    def bot(self):
        return Bus.byorig(self.orig)

    def parse(self):
        if self.txt is not None:
            parse_txt(self, self.txt)

    def ready(self):
        self.done.set()

    def reply(self, txt):
        self.result.append(txt)

    def say(self, txt):
        Bus.say(self.orig, self.channel, txt.rstrip())

    def show(self):
        if self.exc:
            self.say(self.exc)
            return
        bot = self.bot()
        if not bot:
            raise NoBot(self.orig)
        if bot.speed == "slow" and len(self.result) > 3:
            Output.append(self.channel, self.result)
            self.say("%s lines in cache, use !mre" % len(self.result))
            return
        for txt in self.result:
            self.say(txt)

    def wait(self, timeout=1.0):
        self.done.wait(timeout)
        for thr in self.thrs:
            thr.join(timeout)

class Command(Event):

    def __init__(self):
        super().__init__()
        self.type = "cmd"

class Loop(ob.Object):

    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.speed = "normal"
        self.stopped = threading.Event()

    def do(self, e):
        raise NotImplemented("do")
        
    def error(self, e):
        raise NotImplemented("error")

    def loop(self):
        dorestart = False
        self.stopped.clear()
        while not self.stopped.isSet():
            e = self.queue.get()
            try:
                self.do(e)
            except Restart:
                dorestart = True
                break
            except Stop:
                break
            except Exception as ex:
                e = Event()
                e.type = "error"
                e.exc = ex
                self.error(e)
        if dorestart:
            self.restart()

    def restart(self):
        self.stop()
        self.start()

    def put(self, e):
        self.queue.put_nowait(e)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        ob.launch(self.loop)
        return self

    def stop(self):
        self.stopped.set()
        self.queue.put(None)

class Handler(Dispatcher, Loop):

    def cmd(self, txt):
        Bus.add(self)
        e = self.event(txt)
        e.origin = "root@shell"
        self.dispatch(e)
        e.wait()

    def event(self, txt):
        if txt is None:
            return
        c = Command()
        c.txt = txt or ""
        c.orig = self.__dorepr__()
        return c

    def handle(self, e):
        raise NotImplemented("handle")

    def loop(self):
        while not self.stopped.isSet():
            txt = self.poll()
            if txt is None:
                break
            e = self.event(txt)
            if not e:
                break
            self.handle(e)

    def poll(self):
        return self.queue.get()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        super().start()
        Bus.add(self)
