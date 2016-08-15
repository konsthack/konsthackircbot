#!/usr/bin/env python2.7

# ircecho.py
# Copyright (C) 2011 : Robert L Szkutak II - http://robertszkutak.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import socket
import string
import time 
import urllib2

HOST = "irc.freenode.net"
PORT = 6667

NICK = "artbot"
IDENT = "artbot"
REALNAME = "palle"
MASTER = "plix"
MESSAGE = "hello konsthack"
readbuffer = ""

s=socket.socket( )
s.connect((HOST, PORT))

s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN #konsthack\r\n");
s.send("PRIVMSG %s :Hello Master\r\n" % MASTER)
s.send("PRIVMSG #konsthack : %s\r\n" % MESSAGE)


def getmessages(): 
    link = "https://raw.githubusercontent.com/konsthack/konsthackircbot/master/messages.rm"
    data = urllib2.urlopen(link)
    for the_message in data.readlines():
        s.send("PRIVMSG #konsthack : %s\r\n" % the_message)

    print ("messages")

 
while 1:
    readbuffer = readbuffer+s.recv(1024)
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        if(line[1] == "PRIVMSG"):
            sender = ""
            for char in line[0]:
                if(char == "!"):
                    break
                if(char != ":"):
                    sender += char 
            size = len(line)
            i = 3
            message = ""
            while(i < size): 
                message += line[i] + " "
                i = i + 1
            message.lstrip(":")
            s.send(bytes("PRIVMSG %s %s \r\n" % (sender, message), "UTF-8"))
        for index, i in enumerate(line):
            print(line[index])
        getmessages()
        time.sleep(100)
