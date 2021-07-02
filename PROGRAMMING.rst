PROGRAMMING
###########

this is the programmer's manual.

programming
===========

the bot package provides a library you can use to program objects under python3.
It provides a basic Object, that mimics a dict while using attribute access
and provides a save/load to/from json files on disk. objects can be searched
with a little database module, it uses read-only files to improve persistence
and a type in filename for reconstruction.

basic usage is this::

 >>> from bot.obj import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

the bot.obj module has the basic methods like load and save as a object
function using an obj as the first argument::

 >>> import bot.obj
 >>> bot.obj.wd = "data"
 >>> o = bot.obj.Object()
 >>> o["key"] = "value"
 >>> p = o.save()
 >>> p
 'bot.obj.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
 >>> oo = bot.obj.Object()
 >>> oo.load(p)
 >> oo.key
 'value'

great for giving objects peristence by having their state stored in files.

commands
========

modules are not read from a directory, instead you must include your own
written commands with a updated version of the code. First clone the
repository (as user)::

 $ git clone http://github.com/bthate/botd
 $ cd botd
 
to program your own commands, open bot/hlo.py (new file) and add the following
code::

    def register(k):
        k.regcmd(hlo)

    def hlo(event):
        event.reply("hello %s" % event.origin)

add the hlo module to the bot/all.py module::

    import bot.hlo

    Kernel.addmod(bot.hlo)

edit the list of modules to load in bin/botd::

    all = "adm,cms,fnd,irc,krn,log,rss,tdo,hlo"

then install with python3 (using sudo)::

 $ python3 setup.py install
 $ python3 setup.py install_data

reload the systemd service::

 $ systemctl stop botd
 $ systemctl start botd

now you can type the "hlo" command, showing hello <user>::

 <bart> !hlo
 hello root@console

