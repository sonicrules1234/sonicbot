import glob, imp, os, traceback, time, shelve
minlevel = 1
arguments = ["self", "info", "world"]
keyword = "PRIVMSG"
def main(self, info, world) :
    """This is the essentials"""
    """Is executed when sonicbot receives the PRIVMSG command"""
    if info["message"] == "\x01VERSION\x01" :
        self.notice(info["sender"], "\x01VERSION sonicbotv4 Development Version https://github.com/sonicrules1234/sonicbot\x01")
    if info["message"] == "\x01TIME\x01" :
        self.notice(info["sender"], "\x01 TIME %s\x01" % (time.strftime("%b %d %Y, %H:%M:%S %Z")))
    args = info["message"].split(" ")
    conf = self

    if args == [] :
        args.append("")
    if info["message"][:len(self.trigger)] == self.trigger :
        args[0] = args[0][1:]
        triggered = True
    elif args[0] == self.nick + ":" or args[0] == self.nick + "," :
        triggered = True
        args = args[1:]
        if args == [] :
            args.append("")
    else : triggered = False
    if triggered :
        if world.plugins.has_key(args[0].lower()) :
            for plugin in world.plugins[args[0].lower()] :
                arguments = eval(", ".join(plugin["arguments"]))
                if info["channel"] != info["sender"] :
                    if self.allowed(info, plugin["minlevel"]) and args[0].lower() in self.users["channels"][info["channel"]]["enabled"] :
                        try :
                            plugin["function"](*arguments)
                        except :
                            self.error = traceback.format_exc()
                            self.msg(info["channel"], "Error")
                            print self.error
                elif info["channel"] == info["sender"] :
                    if self.allowed(info, plugin["minlevel"]) :
                        try :
                            plugin["function"](*arguments)
                        except :
                            self.error = traceback.format_exc()
                            self.msg(info["channel"], "Error")
                            print self.error
        elif info["sender"] == info["channel"] :
            try :
                if isfactoid(info["message"][len(self.trigger):]) :
                    self.msg(info["channel"], getfactoid(info["message"][len(self.trigger):], info))
            except: traceback.print_exc()            
        elif args[0].lower() not in self.users["channels"][info["channel"]]["enabled"] :
            try :
                if isfactoid(info["message"][len(self.trigger):]) and not self.isignored(info) :
                    self.msg(info["channel"], getfactoid(info["message"][len(self.trigger):], info))
            except: traceback.print_exc()
def isfactoid(fact) :
    factoids = shelve.open("factoids.db")
    args = fact.split(" ")
    x = fact.split(" | ")
    if factoids.has_key(args[0].lower()) :
        return True
    else : return False
def getfactoid(fact, info) :
    factoids = shelve.open("factoids.db")
    args = fact.split(" ")
    x = fact.split(" | ", 1)
    if factoids[args[0].lower()].has_key(info["channel"]) :
        message = ""
        if len(x) == 2 :
            message = x[1] + ": "
        message += factoids[args[0].lower()][info["channel"]]["definition"]
        return message
    else : return "No such command or factoid."
