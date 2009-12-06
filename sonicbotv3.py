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
if world.pythonversion == "2.6" :
    import ssl
class sonicbot :
        
        
    def connect(self) :
        print "So far so good"
        try :
            self.sock.connect((self.host, self.port))
            if conf.ssl[conf.hosts.index(self.host)] and world.pythonversion == "2.5" :
                self.sock = socket.ssl(self.sock)
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
        except :
            errorlog = open("errorlog.txt", "a")
            errorlog.write(traceback.format_exc() + "\n")
            errorlog.close()
            traceback.print_exc()
        print "Connected to", self.host
        try :
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
            self.chanmodes = {}
            self.users = shelve.open("users-%s.db" % (world.hostnicks[self.host]), writeback=True)
            if not self.users.has_key("users") :
                self.users["users"] = {}
                self.users.sync()
                for admin in conf.admin.keys() :
                    self.users["users"][admin] = {"userlevel":4, "hostname":conf.admin[admin]}
                    self.users.sync()
                self.users["users"][conf.owner]["userlevel"] = 5
                self.users.sync()
            if not self.users.has_key("channels") :
                self.users["channels"] = {}
                self.users.sync()
            if not self.users.has_key("hostignores") :
                self.users["hostignores"] = []
                self.users.sync()
            self.timer = 0
        except : traceback.print_exc()
        self.startLoop()

    def start(self, host, port) :
        try :
            self.host = host
            self.port = port
            if conf.ipv6[conf.hosts.index(self.host)] :
                self.iptype = socket.AF_INET6
            else :
                self.iptype = socket.AF_INET
            self.sock = socket.socket(self.iptype, socket.SOCK_STREAM)
            if conf.ssl[conf.hosts.index(self.host)] :
                if world.pythonversion == "2.6" :
                    self.sock = ssl.wrap_socket(self.sock)
        except :
            errorlog = open("errorlog.txt", "a")
            errorlog.write(traceback.format_exc() + "\n")
            errorlog.close()
            traceback.print_exc()
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
                        if self.host in conf.connectcommands :
                            for command in conf.connectcommands[self.host] :
                                exec(command)
                    info["whois"] = info["words"][0]
                    info["sender"] = info["whois"].split("!")[0]
                except : traceback.print_exc()
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
        if conf.ssl[conf.hosts.index(self.host)] and world.pythonversion == "2.5" :
            self.sock.write(msg_out)
        else :
            self.sock.send(msg_out)
        if conf.debug : print "[OUT]%s" % (msg_out)
    def startLoop(self) :
        socketerror = False
        while not socketerror :
            if conf.ssl[conf.hosts.index(self.host)] and world.pythonversion == "2.5" :
                try :
                    data = self.sock.read()
                    socketerror = False
                except : socketerror = True
                if not socketerror :
                    self.dataReceived(data)
            else :
                try :
                    data = self.sock.recv(4096)
                except : socketerror = True
                if not socketerror : self.dataReceived(data)
        print "connection lost"
        self.logf.close()
        for channel in self.channels :
            self.logs[channel].close()
        del world.connections[self.host]
        print repr(world.connections)
        conf.ports.pop(conf.hosts.index(self.host))
        conf.ssl.pop(conf.hosts.index(self.host))
        conf.hosts.remove(self.host)
        del conf.channels[self.host]
        world.hostcount -= 1
        self.sock.close()
    def on_ACTION(self, info, args) :
        self.logwrite(info["channel"], "[%s] *%s %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], " ".join(args[1:]).replace("", "")))
        if not conf.debug : "[%s] *%s %s\n" % (time.strftime("%H:%M:%S"), info["sender"], " ".join(args[1:]).replace("", ""))
        if "on_ACTION" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_ACTION"].main(self, info, conf)

    def on_TIME(self, info) :
        if "on_TIME" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_TIME"].main(self, info, conf)

    def on_VERSION(self, info) :
        self.rawsend("NOTICE %s :VERSION SonicBot version 3.2.0\n" % (info["sender"]))

    def on_PRIVMSG(self, info) :
        if not info["channel"].startswith("#") :
            if info["channel"] in self.users["channels"] :
                if self.users["channels"][info["channel"]]["registered"] :
                    pass
                else :
                    self.users["channels"][info["channel"]]["enabled"] = []
                    self.users.sync()
                    for plugin in self.plugins["pluginlist"].pluginlist :
                        self.users["channels"][info["channel"]]["enabled"].append(plugin)
                        self.users.sync()
            else :
                self.users["channels"][info["channel"]] = {"registered":False, "enabled":[]}

                self.users.sync()
                for plugin in self.plugins["pluginlist"].pluginlist :
                    self.users["channels"][info["channel"]]["enabled"].append(plugin)
                    self.users.sync()
        if info["channel"] in self.channels : self.logwrite(info["channel"], "[%s] <%s> %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["message"]))
        if not info["message"]: return
        if info["message"][0] == conf.prefix or info["message"].split(" ")[0] == conf.nick + ":" :
            self.command_parser(info)
        if "on_PRIVMSG" in self.plugins["pluginlist"].eventlist:
            self.plugins["on_PRIVMSG"].main(self, info, conf)

    def on_JOIN(self, info) :
        if conf.nick == info["sender"] :
            self.logs[info["channel"]] = open("logs/%s.txt" % (info["channel"]), "a")
            self.channels[info["channel"]] = []
            self.chanmodes[info["channel"]] = {}
            if info["channel"] in self.users["channels"] :
                if self.users["channels"][info["channel"]]["registered"] :
                    pass
                else :
                    self.users["channels"][info["channel"]]["enabled"] = []
                    self.users.sync()
                    for plugin in self.plugins["pluginlist"].pluginlist :
                        self.users["channels"][info["channel"]]["enabled"].append(plugin)
                        self.users.sync()
            else :
                self.users["channels"][info["channel"]] = {"registered":False, "enabled":[]}

                self.users.sync()
                for plugin in self.plugins["pluginlist"].pluginlist :
                    self.users["channels"][info["channel"]]["enabled"].append(plugin)
                    self.users.sync()
        else : self.channels[info["channel"]].append(info["sender"])
        self.chanmodes[info["channel"]][info["sender"]] = []
        self.logwrite(info["channel"], "[%s] ***%s has joined %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["channel"]))
        if "on_JOIN" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_JOIN"].main(self, info, conf)
        if info["sender"] == conf.nick : self.rawsend("WHO %s\n" % (info["channel"]))

    def on_PART(self, info) :
        self.logwrite(info["channel"], "[%s] ***%s has parted %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["channel"]))
        if conf.nick == info["sender"] :
            self.logs[info["channel"]].close()
            del self.channels[info["channel"]]
            del self.chanmodes[info["channel"]]
        else : self.channels[info["channel"]].remove(info["sender"])
        if "on_PART" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_PART"].main(self, info, conf)

    def on_QUIT(self, info) :
        quitmessage = " ".join(info["words"][2:])[1:]
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
        self.channels[info["channel"]].remove(recvr)
        if "on_KICK" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_KICK"].main(self, info, conf)

    def on_TOPIC(self, info) :
        self.logwrite(info["channel"], '[%s] **%s has changed the topic in %s to "%s"\n' % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["channel"], info["message"]))
        if "on_TOPIC" in self.plugins["pluginlist"].eventlist :
            self.plugins["on_TOPIC"].main(self, info, conf)

    def on_MODE(self, info) :
        mode = info["words"][3]
        modesymbols = {"y":"!", "h":"%", "o":"@", "v":"+", "F":"~", "q":"~", "a":"&"}
        if len(info["words"]) > 4 :
            recvrs = info["words"][4:]
            recvr = 0
            self.logwrite(info["channel"], "[%s] **%s set mode %s on %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], mode, " ".join(recvrs)))
            for letter in mode:
                if letter == "+" : modetype = True
                elif letter == "-" : modetype = False
                else :
                    if letter in modesymbols.keys() :
                        print self.host
                        if modetype :
                            if letter not in self.chanmodes[info["channel"]][recvrs[recvr]] :
                                self.chanmodes[info["channel"]][recvrs[recvr]].append(modesymbols[letter])
                        elif not modetype :
                            if letter in self.chanmodes[info["channel"]][recvrs[recvr]] :
                                self.chanmodes[info["channel"]][recvrs[recvr]].remove(letter)
                        recvr += 1
        else :
            self.logwrite(conf.nick, "[%s] **%s set mode %s on %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], mode, info["channel"]))
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
                self.chanmodes[channel][newnick] = self.chanmodes[channel][info["sender"]]
                del self.chanmodes[channel][info["sender"]]
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
                newnick = nick.replace(":", "")
                for mode in ["!", "%", "@", "&", "~", "+"] :
                    newnick = newnick.replace(mode, "")
                self.chanmodes[info["words"][4].lower()][newnick] = []
                if newnick == conf.nick : print "Yep", newnick, self.host
                for mode in ["!", "%", "@", "&", "~", "+"] :
                    if mode in correctnick :
                        self.chanmodes[info["words"][4].lower()][newnick].append(mode)
                correctnick = newnick
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
                self.plugins['on_%s' % info["mode"]].main(self, info, conf)
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
                if args[3] == "1" :
                    conf.ssl.append(True)
                else : conf.ssl.append(False)
                if args[4] == "1" :
                    conf.ipv6.append(True)
                else : conf.ipv6.append(False)
                world.hostnicks[args[1]] = args[5]
                conf.channels[args[1]] = args[6:]
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
                    if args[1] in self.nicks :
                        if self.nicks[args[1]] not in conf.hostignores :
                            conf.hostignores.append(self.nicks[args[1]])
                    self.ircsend(info["channel"], "%s will now be ignored" % (args[1]))
                else : self.ircsend(info["channel"], "I will never ignore my owner!")
            elif args[0] == "-ignore" :
                if args[1] in conf.ignorelist and info["sender"] == conf.owner and info["hostname"] in conf.admin[info["sender"]] :
                    conf.ignorelist.remove(args[1])
                    if args[1] in self.nicks :
                        if self.nicks[args[1]] in conf.hostignores :
                            conf.hostignores.remove(self.nicks[args[1]])
                    self.ircsend(info["channel"], "%s has been removed from the ignore list" % (args[1]))
                else : self.ircsend(info["channel"], "No such nick in the ignore list!")
            elif args[0] == "reload" :
                for filename in glob.glob("plugins/*.pyc") :
                    os.remove(filename)
                temphosts = conf.hosts
                tempports = conf.ports
                tempssl = conf.ssl
                tempipv6 = conf.ipv6
                tempignorelist = conf.ignorelist
                temphostignores = conf.hostignores
                reload(conf)
                conf.hosts = temphosts
                conf.ports = tempports
                conf.ssl = tempssl
                conf.ipv6 = tempipv6
                conf.ignorelist = tempignorelist
                conf.hostignores = temphostignores
                self.oldplugins = self.plugins.copy()
                self.plugins = {}
                print repr(self.plugins)
                for plugin in glob.glob("plugins/*.py") :
                    if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" :
                        self.plugins[plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "")] = imp.load_source(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""), plugin)
                channels = self.users["channels"]
                for plugin in self.oldplugins["pluginlist"].pluginlist :
                    if plugin not in self.plugins["pluginlist"].pluginlist :
                        
                        temp = self.users["channels"].keys()
                        for channel in temp :
                            if plugin in self.users["channels"]["enabled"] :
                                channels[channel]["enabled"].remove(plugin)
                self.users["channels"] = channels
                self.users.sync()
                del self.oldplugins
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
                    arguments = eval(", ".join(self.plugins[args[0]].arguments))
                    if args[0] in self.users["channels"][info["channel"]]["enabled"] :
                        if self.auth(info, self.plugins[args[0]].minlevel) :
                            self.plugins[args[0]].main(*arguments)
                        else : self.ircsend(info["channel"], "%s: You do not have a high enough user level and/or privleges in this channel to use that command!" % (info["sender"]))
                    else : self.ircsend(info["channel"], "That plugin is not enabled in this channel.  To enable it, use ;enable %s" % (args[0]))
                except: 
                    traceback.print_exc()
                    self.ircsend(info["channel"], "Error.  The syntax for that command is: %s" % (eval("self.plugins['%s'].helpstring" % (args[0]))))
            elif notacommand or notacommand2 :
                pass

    def ircfilter(self, string, bads=[]) :
        for bad in bads :
            string = string.replace(bad, "")
        return string

    def auth(self, info, minlevel) :
        if info["sender"] not in self.users["users"].keys() :
            self.users["users"][info["sender"]] = {"hostname":[self.nicks[info["sender"]]], "userlevel":1}
            self.users.sync()
        else :
            if self.users["users"][info["sender"]]["userlevel"] in [0, 1] :
                self.users["users"][info["sender"]]["hostname"].append(self.nicks[info["sender"]])
                self.users.sync()
            if info["hostname"] in self.users["users"][info["sender"]]["hostname"] :
                if self.users["users"][info["sender"]]["userlevel"] >= minlevel :
                    if minlevel != 3 : return True
                    else :
                        if self.users["users"][info["sender"]].has_key("channels") :
                            if info["channel"] in self.users["users"][info["sender"]]["channels"] :
                                return True
                            else : return False
                        else : return False
                else : return False
            else :
                self.ircsend(info["sender"], "Your nick does not match your hostname.  If you are the owner of this nick, you need to use the addhost command.")
                return False
                        

    def threadedrawsend(self, msg_out, timer) :
        time.sleep(timer)
        if self.host in world.connections.keys() : self.rawsend(msg_out)
    def ircsend(self, targ_channel, msg_out) :
        for line in msg_out.split("\n") :
            length = len("PRIVMSG %s :\n" % (targ_channel))
            parts = []
            current = ""
            for char in line :
                if len(current) + length < 400:
                    current += char
                else :
                    parts.append(current)
                    current = char
            if current != "" :
                parts.append(current)
            for part in parts :
                now = time.time()
                if now > self.timer :
                    self.timer = now + .8
                else : self.timer += .8
                extra = self.timer - now
                if targ_channel.startswith("#") or targ_channel.lower().endswith("serv") : thread.start_new_thread(self.threadedrawsend, ("PRIVMSG %s :%s\n" % (targ_channel, self.ircfilter(part, conf.bads)), extra))
                else : thread.start_new_thread(self.threadedrawsend, ("NOTICE %s :%s\n" % (targ_channel, self.ircfilter(part, conf.bads)), extra))
                if line.startswith("\x01ACTION") : self.logwrite(targ_channel, "[%s] *%s %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), conf.nick, " ".join(part.split(" ")[1:]).replace("\x01", "")))
                else : self.logwrite(targ_channel, "[%s] <%s> %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), conf.nick, self.ircfilter(part, conf.bads)))
            
    
        
    def logwrite(self, channel, log) :
        if channel in self.channels :
            self.logs[channel].write(log)
            if not conf.debug : print log
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


