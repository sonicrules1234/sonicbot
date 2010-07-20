
import json, ssl, select, world, socket, thread, time, traceback, imp, glob, shelve
import gettext, hookstartup, traceback, os
lang = gettext.translation("english", "./locale", languages=["en"])
lang.install()
world.loaded = False
class sonicbot() :
    def __init__(self, networkname, nick, ident, realname, host, port, channels, ssl, ipv6, password, trigger, owner, admin) :
        self.nick = nick
        self.ident = ident
        self.realname = realname
        self.host = host
        self.channels = channels
        self.ssl = ssl
        self.ipv6 = ipv6
        self.password = password
        self.trigger = trigger
        self.port = port
        self.networkname = networkname.lower()
        self.buffer = ""
        self.owner = owner
        self.admin = admin
        self.ignorelist = []
        self.hostignores = []
        if self.ipv6 :
            self.socktype = socket.AF_INET6
        else : self.socktype = socket.AF_INET
        if not world.loaded :
            hookstartup.main(self, world)
        if self.networkname not in glob.glob("*") :
            os.mkdir(self.networkname)
        self.debug = False
    def logwrite(self, channel, log) :
        """Logs things to file, also is used when relaying"""
        if channel in self.channellist :
            self.logs[channel].write(log)
            print log
            if channel != self.nick :
                if channel in world.relay_channels :
                    for server in world.connections.keys() :
                        if server != self.host and channel in world.connections[server].channels :
                            world.connections[server].rawsend("PRIVMSG %s :[%s] %s\n" % (channel, world.hostnicks[self.host], log.split("] ", 1)[1]))
                self.logs[channel].close()
                self.logs[channel] = open("%s/%s.txt" % (self.networkname, channel), "a")
        else : self.logs[self.nick].write(log)
#        self.addHook("PRIVMSG", imp.load_source("essentials/on_PRIVMSG.py", "on_PRIVMSG").main, 1, ["self", "info", "world"])
    def onConnect(self) :
        self.nicksend(self.nick)
        self.usersend(self.ident, self.realname)
        world.instances[self.sock] = self
        world.connections[self.networkname] = self
        world.conlist.append(self.sock)
        self.logs = {}
        self.logs[self.nick] = open("PMs.txt", "a")
        self.chanmodes = {}
        self.channellist = {}
        self.hostnames = {}
        self.users = shelve.open("users-%s.db" % (self.networkname), writeback=True)
        if not self.users.has_key("users") :
            self.users["users"] = {}
            self.users.sync()
            for admin in self.admin.keys() :
                self.users["users"][admin] = {"userlevel":4, "hostname":self.admin[admin]}
                self.users.sync()
            self.users["users"][self.owner]["userlevel"] = 5
            self.users.sync()
        if not self.users.has_key("channels") :
            self.users["channels"] = {}
            self.users.sync()
        if not self.users.has_key("hostignores") :
            self.users["hostignores"] = []
            self.users.sync()
        self.timer = 0
        if not world.waitingfordata :
            world.waitingfordata = True
            thread.start_new_thread(waitfordata, ())
    def enable_all_plugins(self, info) :
        """Enables all plugins for the current channel"""
        self.users["channels"][info["channel"]]["enabled"] = []
        self.users.sync()
        for plugin in world.plugins.keys() :
            self.users["channels"][info["channel"]]["enabled"].append(plugin)
            self.users.sync()
    def ircsend(self, channel, message) :
        return self.msg(channel, message)
    def hookOldPlugins(self) :
        oldplugins = {}
        for filename in glob.glob("oldplugins/*.pyc") :
            os.remove(filename)
        for plugin in glob.glob("oldplugins/*.py") :
            if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" :
                oldplugins[plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "")] = imp.load_source(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""), plugin)

    def addHook(self, keyword, function, minlevel, arguments) :
        if not world.hooks.has_key(keyword) :
            world.hooks[keyword] = []
        world.hooks[keyword].append({"minlevel":minlevel, "arguments":arguments, "function":function})

    def connect(self) :
        self.sock = socket.socket(self.socktype, socket.SOCK_STREAM)
        if self.ssl :
            self.sock = ssl.wrap_socket(self.sock)
        self.sock.connect((self.host, self.port))
        self.onConnect()
    def rawsend(self, data) :
        self.sock.send(data)
        print "[OUT %s] %s" % (self.host, data)
    def join(self, channel) :
        self.rawsend("JOIN %s\r\n" % (channel))
    def msg(self, channel, message, reply=False) :
        if reply : message = self.info["sender"] + ": " + message
        if channel.startswith("#") :
            self.pm(channel, message)
        else : self.notice(channel, message)
    def pm(self, channel, message, reply=False) :
        if reply : message = self.info["sender"] + ": " + message
        for line in message.replace("\r", "").split("\n") :
            lines2 = self.quantify("PRIVMSG", channel, line)
            for line2 in lines2 :
                self.determineTiming(channel, line2, "PRIVMSG")        

    def msg2send(self, channel, message) :
        self.rawsend("PRIVMSG %s :%s\r\n" % (channel, message))
    def notice2send(self, channel, message) :
        self.rawsend("NOTICE %s :%s\r\n" % (channel, message))
    def quantify(self, command, channel, message) :
        maxout = 400
        newmaxout = 400 - len("%s %s :\r\n" % (command, channel))
        lines = []
        while message != "" :
            lines.append(message[:newmaxout])
            message = message[newmaxout:]
        return lines
    def notice(self, channel, message, reply=False) :
        if reply : message = self.info["sender"] + ": " + message
        for line in message.replace("\r", "").split("\n") :
            lines2 = self.quantify("NOTICE", channel, line)
            for line2 in lines2 :
                self.determineTiming(channel, line2, "NOTICE")
    def determineTiming(self, channel, line, msgtype) :
        if msgtype == "PRIVMSG" :
            function = self.msg2send
        else :
            function = self.notice2send
        if world.time >= self.timer :
            world.timer.append([world.time + 1, {"function":function, "arguments":(channel, line)}])
            self.timer = world.time + 1
        elif world.time < self.timer :
            world.timer.append([self.timer + 1, {"function":function, "arguments":(channel, line)}])
            self.timer += 1
    def part(self, channel, reason=None) :
        if reason == None :
            self.rawsend("PART %s\r\n" % (channel))
        else :
            self.rawsend("PART %s :%s\r\n" % (channel))
    def usersend(self, ident, realname) :
        self.rawsend("USER %s * * :%s\r\n" % (ident, realname))
    def nicksend(self, nick) :
        self.rawsend("NICK %s\r\n" % (nick))
    
    def dataReceived(self, data):
        """Parses the data into a dict named info"""
        print "[IN %s]" % (self.host) + data
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
                        self.rawsend("MODE %s +B\n" % (self.nick))
                        self.pm("NickServ", "IDENTIFY %s" % (self.password))
                        for i in self.channels :
                            self.rawsend("JOIN %s \n" % (i))
                        #if self.host in conf.connectcommands :
                        #    for command in conf.connectcommands[self.host] :
                        #        exec(command)
                    info["whois"] = info["words"][0]
                    info["sender"] = info["whois"].split("!")[0]
                except : traceback.print_exc()
                try : 
                    info["hostname"] = info["whois"].split("@")[1]
                    self.hostnames[info["sender"]] = info["hostname"]
                except : info["hostname"] = "Unknown"
                try : info["mode"] = info["words"][1]
                except : info["mode"] = "Unknown"
                try :
                    if info["words"][2] == self.nick :
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
    def prettify(self, info) :
#        print repr(world.hooks)
        if world.hooks.has_key(info["mode"]) :
            for hook in world.hooks[info["mode"]] :
                arguments = eval(", ".join(hook["arguments"]))
                hook["function"].main(*arguments)
        if info["mode"] == "PRIVMSG" :
            if info["message"].split(" ")[0] == self.trigger + "reload" and self.allowed(info, 5) :
                del world.plugins
                del world.hooks
                world.hooks = {}
                world.plugins = {}
                hookstartup.main(self, world)
                self.msg(info["channel"], "Plugins reloaded")
            elif info["message"].split(" ")[0] == self.trigger + "connect" and self.allowed(info, 5) :
                try :
                    args = info["message"].split(" ")
                    admin = {self.owner:args[6]}
                    host = args[1]
                    port = int(args[2])
                    if args[3] == "1" :
                        ssl = True
                    else : ssl = False
                    if args[4] == "1" :
                        ipv6 = True
                    else : ipv6 = False
                    networkname = args[5].lower()
                    channels = args[7:]
                    makeNewConnection(networkname, self.nick, self.ident, self.realname, host, port, channels, ssl, ipv6, self.password, self.trigger, self.owner, admin)
                except : traceback.print_exc()
    def allowed(self, info, minlevel) :
        """Authenticates users"""
        if info["sender"] not in self.users["users"].keys() :
            self.users["users"][info["sender"]] = {"hostname":[self.hostnames[info["sender"]]], "userlevel":1}
            self.users.sync()
        if self.users["users"][info["sender"]]["userlevel"] in [0, 1] and self.hostnames[info["sender"]] not in self.users["users"][info["sender"]]["hostname"]:
            self.users["users"][info["sender"]]["hostname"].append(self.hostnames[info["sender"]])
            self.users.sync()
        if info["hostname"] in self.users["users"][info["sender"]]["hostname"] or minlevel == 1 :
            if self.users["users"][info["sender"]]["userlevel"] >= minlevel :
                if minlevel != 3 or self.users["users"][info["sender"]]["userlevel"] in [4, 5] : return True
                else :
                    if self.users["users"][info["sender"]].has_key("channels") :
                        if info["channel"] in self.users["users"][info["sender"]]["channels"] :
                            return True
                        else : return False
                    else : return False
            else : return False
        else :
            self.ircsend(info["sender"], _("Your nick does not match your hostname.  If you are the owner of this nick, you need to use the addhost command."))
            return False

def floodControl() :
    while True :
        currenttime = world.time
        worldtimer = world.timer[:]
        for x in worldtimer :
            if x[0] < currenttime :
                world.timer.pop(0)
            elif x[0] == currenttime :
                x[1]["function"](*x[1]["arguments"])
            else :
                break
        del worldtimer
        time.sleep(1)
        world.time += 1

def waitfordata() :
    world.timer = []
    world.time = 0
    thread.start_new_thread(floodControl, ())
    """Actual loop of waiting for data and parsing it"""
    while True :
        noerror = False
        tempconlist = world.conlist[:]
        try :
            connections = select.select(tempconlist, [], [], 5)
            noerror = True
        except :
            for network in tempconlist :
                try :
                    connections = select.select([network], [], [], 0)
                except :
                    del world.connections[world.instances[connection].networkname]
                    del world.instances[network]
                    world.conlist.remove(network)

        if noerror :
            for connection in connections[0] :
                try : data = connection.recv(4096)
                except :
                    traceback.print_exc()
                    data = ""
                if data != "" :
                    world.instances[connection].dataReceived(data)
                else:
                    print "No data, closing the connection"
                    del world.connections[world.instances[connection].networkname]
                    del world.instances[connection]
                    world.conlist.remove(connection)
                    connection.close()
        del tempconlist

def makeNewConnection(networkname, nick, ident, realname, host, port, channels, ssl, ipv6, password, trigger, owner, admin) :
    v = sonicbot(networkname, nick, ident, realname, host, port, channels, ssl, ipv6, password, trigger, owner, admin)
    v.connect()
conffile = open("conf.json", "r")
conf = conffile.read()
conffile.close()
jsonconf = json.loads(conf)

for network in jsonconf :
    newconf = {}
    newconf["nick"] = network[u"nick"].encode("utf8")
    newconf["ident"] = network[u"ident"].encode("utf8")
    newconf["realname"] = network[u"realname"].encode("utf8")
    newconf["host"] = network[u"host"].encode("utf8")
    newconf["channels"] = [channel.encode("utf8") for channel in network[u"channels"]]
    newconf["ssl"] = network[u"ssl"]
    newconf["ipv6"] = network[u"ipv6"]
    newconf["password"] = network[u"password"].encode("utf8")
    newconf["trigger"] = network[u"trigger"].encode("utf8")
    newconf["port"] = network[u"port"]
    newconf["networkname"] = network[u"networkname"].encode("utf8").lower()
    newconf["owner"] = network[u"owner"].encode("utf8")
    newconf["admin"] = {}
    for nick in network[u"admin"] :
        newconf["admin"][nick.encode("utf8")] = network[u"admin"][nick]

    a = sonicbot(**newconf)
    a.connect()
#a = sonicbot("vbirc", "sonicbot-dev", "sonicbot-dev", "Development version of sonicbotv4", "2a02:780:d002:5::17", 6697, ["#ninjas"], True, False, "")
#a.connect()
try :
    while True :
        time.sleep(5)
except :
    for network in world.instances.keys() :
        world.instances[network].rawsend("QUIT :Hmm, somebody hit Ctrl-C, better /quit!\n")
        world.instances[network].sock.close()
