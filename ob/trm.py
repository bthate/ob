# This file is placed in the Public Domain.

import atexit
import sys
import termios

def __dir__():
    return ('termsave', 'termreset', 'wrap')

resume = {}

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
