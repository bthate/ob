# This file is placed in the Public Domain.

def __dir__():
    return ('NoClass', 'NoType', 'NoText', 'NoUser', 'Restart', 'Stop')

class NoBot(Exception):

    pass

class NoClass(Exception):

    pass

class NoType(Exception):

    pass

class NoText(Exception):

    pass

class NoUser(Exception):

    pass

class NotImplemented(Exception):

    pass

class Restart(Exception):

    pass

class Stop(Exception):

    pass
