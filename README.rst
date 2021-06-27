README
######

Welcome to OB, the python3 object library.

OB is a pure python3 library you can use to program objects with.

installation is through pypi, use the superuser (sudo)::

 $ pip3 install ob

OB is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

programming
===========

the ob module provides a library you can use to program objects under python3.
It provides a basic BigO Object, that mimics a dict while using attribute access
and provides a save/load to/from json files on disk. Objects can be searched
with a little database module, it uses read-only files to improve persistence
and a type in filename for reconstruction.

basic usage is this::

 >>> from ob import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

the bot.obj module has the basic methods like load and save as a object
function using an obj as the first argument::

 >>> from ob import Object, cfg
 >>> cfg.wd = "data"
 >>> o = Object()
 >>> o["key"] = "value"
 >>> p = o.save()
 >>> p
 'ob.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
 >>> oo = Object()
 >>> oo.load(p)
 >> oo.key
 'value'

great for giving objects peristence by having their state stored in files.

contact
=======

"contributed back"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
