#!/usr/bin/env python

# Copyright (c) 2009, Westly Ward
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Sonicbot Team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY Westly Ward ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Westly Ward BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import time, glob, shelve, traceback, os, aiml, imp
import socket, conf, thread, world
class sonicbot :
    def __init__(self) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self) :
        print "So far so good"
        try :
            self.sock.connect((self.host, self.port))
            self.rawsend("NICK %s \n" % (conf.nick))
            self.rawsend("USER %s * * :%s\n" % (conf.ident, conf.realname))
            self.plugins = {}
            print "Stage1"
            for filename in glob.glob("plugins/*.pyc") :
                os.remove(filename)
            print "stage2"
            for plugin in glob.glob("plugins/*.py") :
                if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" :
                    self.plugins[plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "")] = imp.load_source(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""), plugin)
            print "stage3"
            self.host = conf.hosts[world.hostcount]
            print len(conf.hosts)
            world.connections[self.host] = self
            
            if world.hostcount + 1 != len(conf.channels.keys()) :
                world.hostcount += 1
                new = sonicbot()
                thread.start_new_thread(new.start, (conf.hosts[world.hostcount], conf.ports[world.hostcount]))
        except : traceback.print_exc()
        print "Connected"
        self.logf = open("raw.txt", "a")
        if conf.bpass != "" : self.rawsend("PASS %s\n" % (conf.bpass))
        self.factoids = shelve.open("factoids.db")
        self.channels = {}
        self.logs = {}
        self.logs[conf.nick] = open("logs/PMs.txt", "a")
        if conf.ai :
            self.ai = aiml.Kernel()
            self.ai.learn("std-startup.xml")
            self.ai.setBotPredicate("name", conf.nick)
            self.ai.setBotPredicate("master", conf.owner)
            self.ai.setBotPredicate("gender", "male")
            self.ai.respond("load aiml b")
        self.nicks = {}
        self.buffer = ""
        self.startLoop()

    def start(self, host, port) :
        self.host = host
        self.port = port
        self.connect()

    def dataReceived(self, data):
        if conf.debug :
            print "[IN]" + data

        self.logf.write("[IN]%s" % (data))
        

        error = 0
        lines = data.replace("\r", "").split("\n")
        lines[0] = self.buffer + lines[0]
        self.buffer = lines[-1]
        for line in lines[:-1] :
            if line != "" :
                try: 
                    if line.split(" ")[0] == "PING" : self.rawsend("PONG %s\n" % (line.split(" ")[1]))
                    info = {}
                    info["raw"] = line
                    info["words"] = line[1:].split(" ")
                    if info["words"][1] == "001" :
                        self.rawsend("MODE %s +B\n" % (conf.nick))
                        self.ircsend("NickServ", "IDENTIFY %s" % (conf.bpass))
                        for i in conf.channels[self.host] :
                            self.rawsend("JOIN %s \n" % (i))
                    info["whois"] = info["words"][0]
                    info["sender"] = info["whois"].split("!")[0]
                except : print "ok"
                try : 
                    info["hostname"] = info["whois"].split("@")[1]
                    self.nicks[info["sender"]] = info["hostname"]
                except : info["hostname"] = "Unknown"
                try : info["mode"] = info["words"][1]
                except : info["mode"] = "Unknown"
                try :
                    if info["words"][2] == conf.nick :
                        info["channel"] = info["sender"]
                    else : info["channel"] = info["words"][2].replace(":", "").lower()
                except : info["channel"] = "Unknown"
                try : 
                    if info["mode"] == "PRIVMSG" or info["mode"] == "TOPIC" :
                        if ":" in info["words"][3] : info["message"] = " ".join(info["words"][3:])[1:]
                        else : info["message"] = " ".join(info["words"][3:])
                    else : info["message"] = "Unknown"
                except : error = 1
                self.info = info
                if error != 1 : self.prettify(info)
    def rawsend(self, msg_out) :
        self.sock.send(msg_out)
        print "[OUT]%s" % (msg_out)
    def startLoop(self) :
        data = True
        while data :
            data = self.sock.recv(4096)
            if data : self.dataReceived(data)
        print "connection lost"
        self.logf.close()
        for channel in self.channels :
            self.logs[channel].close()
        del world.connections[self.host]
        conf.ports.pop(conf.hosts.index(self.host))
        conf.hosts.remove(self.host)
        del conf.channels[self.host]
        world.hostcount -= 1		
    def on_ACTION(self, info, args) :
        self.logwrite(info["channel"], "[%s] *%s %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], " ".join(args[1:]).replace("", "")))
        if not conf.debug : "[%s] *%s %s\n" % (time.strftime("%H:%M:%S"), info["sender"], " ".join(args[1:]).replace("", ""))
        if "on_ACTION" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_ACTION"].main(self, info, conf)

    def on_TIME(self, info) :
        if "on_TIME" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_TIME"].main(self, info, conf)

    def on_VERSION(self, info) :
        self.rawsend("NOTICE %s :VERSION SonicBot version 3.1.0\n" % (info["sender"]))

    def on_PRIVMSG(self, info) :
        if info["channel"] in self.channels : self.logwrite(info["channel"], "[%s] <%s> %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["message"]))
        if not conf.debug : print "[%s] <%s> %s\n" % (time.strftime("%H:%M:%S"), info["sender"], info["message"])
        if not info["message"]: return
        if info["message"][0] == conf.prefix or info["message"].split(" ")[0] == conf.nick + ":" :
            self.command_parser(info)
        if "on_PRIVMSG" in self.plugins["pluginlist"].eventlist:
            self.plugins["on_PRIVMSG"].main(self, info, conf)

    def on_JOIN(self, info) :
        if not conf.debug : print "[%s] ***%s has joined %s\n" % (time.strftime("%H:%M:%S"), info["sender"], info["channel"])
        if conf.nick == info["sender"] :
            self.logs[info["channel"]] = open("logs/%s.txt" % (info["channel"]), "a")
            self.channels[info["channel"]] = []
        else : self.channels[info["channel"]].append(info["sender"])
        self.logwrite(info["channel"], "[%s] ***%s has joined %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["channel"]))
        if "on_JOIN" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_JOIN"].main(self, info, conf)
        if info["sender"] == conf.nick : self.rawsend("WHO %s\n" % (info["channel"]))

    def on_PART(self, info) :
        self.logwrite(info["channel"], "[%s] ***%s has parted %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["channel"]))
        if not conf.debug : print "[%s] ***%s has parted %s\n" % (time.strftime("%H:%M:%S"), info["sender"], info["channel"])
        if conf.nick == info["sender"] :
            self.logs[info["channel"]].close()
            del self.channels[info["channel"]]
        else : self.channels[info["channel"]].remove(info["sender"])
        if "on_PART" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_PART"].main(self, info, conf)

    def on_QUIT(self, info) :
        quitmessage = " ".join(info["words"][2:])[1:]
        if not conf.debug : print "[%s] ***%s has quit (%s)\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], quitmessage)
        for channel in self.channels :
            if info["sender"] in self.channels[channel] :
                self.channels[channel].remove(info["sender"])
                self.logwrite(channel, "[%s] ***%s has quit (%s)\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], quitmessage))
                if info["sender"] == conf.nick : self.logs[channel].close()
        if "on_QUIT" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_QUIT"].main(self, info, conf)

    def on_KICK(self, info) :
        recvr = info["words"][3]
        self.logwrite(info["channel"], "[%s] **%s has kicked %s from %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], recvr, info["channel"]))
        if not conf.debug : print "[%s] **%s has kicked %s from %s" % (time.strftime("%H:%M:%S"), info["sender"], recvr, info["channel"])
        self.channels[info["channel"]].remove(recvr)
        if "on_KICK" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_KICK"].main(self, info, conf)

    def on_TOPIC(self, info) :
        self.logwrite(info["channel"], '[%s] **%s has changed the topic in %s to "%s"\n' % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["channel"], info["message"]))
        if not conf.debug : print '[%s] **%s has changed the topic in %s to "%s"' % (time.strftime("%H:%M:%S"), info["sender"], info["channel"], info["message"])
        if "on_TOPIC" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_TOPIC"].main(self, info, conf)

    def on_MODE(self, info) :
        mode = info["words"][3]
        if len(info["words"]) > 4 :
            recvr = info["words"][4]
            self.logwrite(info["channel"], "[%s] **%s set mode %s on %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], mode, recvr))
            if not conf.debug : print "[%s] **%s set mode %s on %s" % (time.strftime("%H:%M:%S"), info["sender"], mode, recvr)
        else :
            self.logwrite(conf.nick, "[%s] **%s set mode %s on %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], mode, info["channel"]))
            if not conf.debug : print "[%s] **%s set mode %s on %s" % (time.strftime("%H:%M:%S"), info["sender"], mode, info["channel"])
        if "on_MODE" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_MODE"].main(self, info, conf)

    def on_NICK(self, info) :
        if ":" in info["words"][2] :
            newnick = info["words"][2][1:]
        else : newnick = info["words"][2]
        self.nicks[newnick] = info["hostname"]
        if not conf.debug : print "[%s]**%s is now known as %s" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["words"][2][1:])
        for channel in self.channels :
            if info["sender"] in self.channels[channel] :
                self.channels[channel].remove(info["sender"])
                self.channels[channel].append(newnick)
                self.logwrite(channel, "[%s] **%s is now known as %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], newnick))
        if "on_NICK" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_NICK"].main(self, info, conf)
        
    def on_INVITE(self, info):
        if "on_INVITE" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_INVITE"].main(self, info, conf)
            
    def on_353(self, info) :
        for nick in info["words"][5:] :
            if nick != "" :
                correctnick = nick.replace(":", "")
                if correctnick[0] in ["%", "@", "&", "~", "+"] :
                    correctnick = correctnick[1:]
                self.channels[info["words"][4].lower()].append(correctnick)
        if "on_353" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_353"].main(self, info, conf)

    def on_352(self, info) :
        self.nicks[info["words"][7]] = info["words"][5]
        if "on_352" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_352"].main(self, info, conf)        

    def prettify(self, info) :
        args = info["message"].split(" ")
        if info["mode"] == "PRIVMSG" :
            if args[0] == "ACTION" :
                self.on_ACTION(info, args)
            elif info["message"] == "VERSION" :
                self.on_VERSION(info)
            elif info["message"] == "TIME" :
                self.on_TIME(info)
            else : 
                self.on_PRIVMSG(info)
        elif info["mode"] == "JOIN" :
            self.on_JOIN(info)
        elif info["mode"] == "PART" :
            self.on_PART(info)
        elif info["mode"] == "QUIT":
            self.on_QUIT(info)
        elif info["mode"] == "KICK" : 
            recvr = info["words"][3]
            self.on_KICK(info)
        elif info["mode"] == "TOPIC" :
            self.on_TOPIC(info)
        elif info["mode"] == "MODE" :
            self.on_MODE(info)
        elif info["mode"] == "INVITE" :
            self.on_INVITE(info)
        elif info["mode"] == "NICK" :
            self.on_NICK(info)
        elif info["mode"] == "353" :
            self.on_353(info)
        elif info["mode"] == "352" :
            self.on_352(info)
        elif "on_%s" % (info["mode"]) in self.plugins["pluginlist"].eventlist :
            try :
                exec("self.plugins['on_%s'].main(self, info, conf)" % (info["mode"]))
            except :
                self.ircsend(conf.owner, traceback.format_exc())
    def command_parser(self, info) :
        notacommand = False
        args = info["message"][1:].split(" ")
        if info["message"].split(" ")[0] == conf.nick + ":" :
            if conf.ai and info["sender"] not in conf.ignorelist and "sing" not in info["message"] :
                response = self.ai.respond(" ".join(args[1:]), info["sender"])
                self.ircsend(info["channel"], "%s: %s" % (info["sender"], response))
            else :
                args = info["message"].split(" ")[1:]
                info["message"] = conf.prefix + " ".join(args)
        if info["message"][0] == conf.prefix and info["sender"] in conf.admin and info["hostname"] in conf.admin[info["sender"]] and info["sender"] not in conf.ignorelist and info["hostname"] not in conf.hostignores :


            if args[0] == "quit" and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]] :
                 self.rawsend("QUIT :Leaving\n")
                 self.sock.close()
            elif args[0] == "add" and " is " in info["message"]:
                if " ".join(args[1:]).split(" is ", 1)[0] not in self.plugins["pluginlist"].pluginlist :
                    self.factoids[" ".join(args[1:]).split(" is ", 1)[0]] = info["message"].split(" is ", 1)[1]
                    self.factoids.sync()
                    self.ircsend(info["channel"], "Factoid %s was successfully added" % (" ".join(args[1:]).split(" is ")[0]))
                else : self.ircsend(info["channel"], "There is already a plugin with that name")
            elif args[0] == "remove" : 
                if self.factoids.has_key(" ".join(args[1:])) :
                    del self.factoids[" ".join(args[1:])]
                    self.factoids.sync()
                    self.ircsend(info["channel"], "Factoid successfully deleted")
                else : self.ircsend(info["channel"], "That factoid does not exist!")
            elif args[0] == "+ai" and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]] :
                conf.ai = True
                self.ai = aiml.Kernel()
                self.ai.learn("std-startup.xml")
                self.ai.setBotPredicate("name", conf.nick)
                self.ai.setBotPredicate("master", conf.owner)
                self.ai.setBotPredicate("gender", "male")
                self.ai.respond("load aiml b")
                self.ircsend(info["channel"], "AI has been turned on")
            elif args[0] == "-ai" and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]] :
                conf.ai = False
                self.ircsend(info["channel"], "AI has been turned off")
            elif args[0] == "+relay" and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]] :
                if info["channel"] not in world.relay_channels :
                    world.relay_channels.append(info["channel"])
                    self.ircsend(info["channel"], "This channel has been added to the relay list")
                else : self.ircsend(info["channel"], "This channel is already on the relay list!")
            elif args[0] == "-relay" and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]] :
                if info["channel"] in world.relay_channels :
                    world.relay_channels.remove(info["channel"])
                    self.ircsend(info["channel"], "This channel has been removed the relay list") 
                else : self.ircsend(info["channel"], "This channel is not on the relay list!")
            elif args[0] == "connect" and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]]:
                conf.hosts.append(args[1])
                conf.ports.append(int(args[2]))
                world.hostcount += 1
                world.hostnicks[args[1]] = args[3]
                conf.channels[args[1]] = args[4:]
                newbotinstance = sonicbot()
                thread.start_new_thread(newbotinstance.start, (args[1], int(args[2])))
            elif args[0] == "eval" and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]] :
                try : self.ircsend(info["channel"], str(eval(" ".join(args[1:]))))
                except : 
                    traceback.print_exc()
                    self.ircsend(info["channel"], "Error")
            elif args[0] == '+ignore' :
                if args[1] != conf.owner :
                    conf.ignorelist.append(args[1])
                    self.ircsend(info["channel"], "%s will now be ignored" % (args[1]))
                else : self.ircsend(info["channel"], "I will never ignore my owner!")
            elif args[0] == "-ignore" :
                if args[1] in conf.ignorelist and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]] :
                    conf.ignorelist.remove(args[1])
                    self.ircsend(info["channel"], "%s has been removed from the ignore list" % (args[1]))
                else : self.ircsend(info["channel"], "No such nick in the ignore list!")
            elif args[0] == "reload" :
                for filename in glob.glob("plugins/*.pyc") :
                    os.remove(filename)
                reload(conf)
                self.plugins = {}
                print repr(self.plugins)
                for plugin in glob.glob("plugins/*.py") :
                    if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" :
                        self.plugins[plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "")] = imp.load_source(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""), plugin)

                self.ircsend(info["channel"], "Config and plugins reloaded.")
            else : notacommand = True
        if info["message"][0] == conf.prefix and info["sender"] not in conf.ignorelist and info["hostname"] not in conf.hostignores:
            notacommand2 = False
            if self.factoids.has_key(info["message"][1:]) :
                self.ircsend(info["channel"], self.factoids[info["message"][1:]])
            elif " | " in info["message"]:
                if self.factoids.has_key(info["message"].split(" | ")[0][1:]) and info["message"].split(" | ", 1)[1].strip() and info["sender"] != info["channel"] :
                    if info["message"].split(" | ", 1)[1].strip() in self.channels[info["channel"]] :
                        self.ircsend(info["channel"], "%s: %s" % (info["message"].split(" | ", 1)[1].strip(), self.factoids[info["message"].split(" | ")[0][1:]]))
                    else : self.ircsend(info["channel"], "%s: %s" % (info["sender"], self.factoids[info["message"].split(" | ")[0][1:]]))
                elif self.factoids.has_key(info["message"].split(" | ")[0][1:]) :
                    self.ircsend(info["channel"], "%s: %s" % (info["sender"], self.factoids[info["message"].split(" | ")[0][1:]]))
                else : notacommand2 = True
            elif args[0] in self.plugins["pluginlist"].pluginlist :
                try :
                    arguments = ", ".join(eval("self.plugins['%s'].arguments" % args[0]))
                    if eval("self.plugins['%s'].needop" % (args[0])) :
                        if info["sender"] in conf.admin and info["hostname"] in conf.admin[info["sender"]] :
                            exec("self.plugins['%s'].main(%s)" % (args[0], arguments))
                        else : self.ircsend(info["channel"], "%s: You do not have enough permissions to use that command!" % (info["sender"]))
                    else : exec("self.plugins['%s'].main(%s)" % (args[0], arguments))
                except: 
                    traceback.print_exc()
                    self.ircsend(info["channel"], "Error.  The syntax for that command is: %s" % (eval("self.plugins['%s'].helpstring" % (args[0]))))
            elif notacommand or notacommand2 :
                pass

    def ircfilter(self, string, bads=[]) :
        for bad in bads :
            string = string.replace(bad, "")
        return string

    def ircsend(self, targ_channel, msg_out) :
        for line in msg_out.split("\n") :
            if targ_channel.startswith("#") or targ_channel.lower().endswith("serv") : self.rawsend("PRIVMSG %s :%s\n" % (targ_channel, self.ircfilter(line, conf.bads)))
            else : self.rawsend("NOTICE %s :%s\n" % (targ_channel, self.ircfilter(line, conf.bads)))
            if line.startswith("\x01ACTION") : self.logwrite(targ_channel, "[%s] *%s %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), conf.nick, " ".join(line.split(" ")[1:]).replace("\x01", "")))
            else : self.logwrite(targ_channel, "[%s] <%s> %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), conf.nick, self.ircfilter(line, conf.bads)))


        
    def logwrite(self, channel, log) :
        if channel in self.channels :
            self.logs[channel].write(log)
            if channel != conf.nick :
                if channel in world.relay_channels :
                    for server in world.connections :
                        if server != self.host and channel in world.connections[server].channels :
                            world.connections[server].rawsend("PRIVMSG %s :[%s] %s\n" % (channel, world.hostnicks[self.host], log.split("] ", 1)[1]))
                self.logs[channel].close()
                self.logs[channel] = open("logs/%s.txt" % (channel), "a")
        else : self.logs[conf.nick].write(log)

if "logs" not in glob.glob("*") :
    os.mkdir("logs")
botinstance = sonicbot()
print "Starting..."
thread.start_new_thread(botinstance.start, (conf.hosts[world.hostcount], conf.ports[world.hostcount]))
while True :
    time.sleep(5)
print "Shutting down..."

