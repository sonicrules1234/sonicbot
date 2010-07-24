import glob, imp, os, traceback, time
minlevel = 1
arguments = ["self", "info", "world"]
keyword = "PRIVMSG"
def main(self, info, world) :
    """This is the essentials"""
    """Is executed when sonicbot receives the PRIVMSG command"""
    if info["message"] == "\x01VERSION\x01" :
        self.notice(info["sender"], "\x01VERSION sonicbotv4 Development Version\x01")
    if info["message"] == "\x01TIME\x01" :
        self.notice(info["sender"], "\x01 TIME %s\x01" % (time.strftime("%b %d %Y, %H:%M:%S %Z")))
    args = info["message"].split(" ")
    conf = self

    if args == [] :
        args.append("")
    if info["message"][0] == self.trigger :
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
                if self.allowed(info, plugin["minlevel"]) and args[0].lower() in self.users["channels"][info["channel"]]["enabled"] :
                    try :
                        plugin["function"](*arguments)
                    except :
                        self.error = traceback.format_exc()
                        self.msg(info["channel"], "Error")
                        print self.error
