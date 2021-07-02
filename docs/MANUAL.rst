MANUAL
######

Welcome to OB, this is the user's manual.

rss
===

with the use of feedparser you canserve rss feeds in your channel (sudo)::

 $ apt install python3-feedparser

add an url use the rss command with an url::

 $ obctl rss https://github.com/bthate/botd/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 $ obctl fnd rss
 0 https://github.com/bthate/botd/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 $ obctl ftc
 fetched 20

udp
===

there is also the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.
output to the IRC channel is done with the use python3 code to send a UDP
packet to BOTD, it's unencrypted txt send to the bot and displayed in the
joined channels::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

to have the udp relay running, add udp to the all variable in bin/botd::

    all = "adm,cms,fnd,irc,krn,log,rss,tdo,udp"

users
=====

if the users option is set in the irc config then users need to be added 
before they can give commands, use the met command to introduce a user::

 $ sudo botctl met ~bart@botd.io
 ok

debug
=====

as of version 42 BOTD uses an internal bot package instead of botl. if you
want to use previous data change botl and botd to bot in /var/lib/botd/store.

contact
=======

"contributed back"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net
|
| OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://genocide.rtfd.io
