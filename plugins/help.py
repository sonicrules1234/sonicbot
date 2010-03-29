helpstring = "help <plugin>"
arguments = ["self", "self.plugins", "args", "info", "conf"]
minlevel = 1
def main(connection, plugs, args, info, conf) :
    """Returns a help message"""
    if " " not in info["message"] :
        connection.ircsend(info["channel"], "%(sender)s: I will notice you a list of my commands, because it is too big to put here." % dict(sender=info["sender"]))
        connection.ircsend(info["sender"], "This bot's prefix is %s  The following is a list of available commands:" % (conf.prefix))
        pluglist = []
        for plug in plugs["pluginlist"].pluginlist :
            if plug in connection.users["channels"][info["channel"]]["enabled"] :
                pluglist.append(plug)
        connection.ircsend(info["sender"], ", ".join(pluglist))
        connection.ircsend(info["sender"], "The help for this module is help <plugin>")
    else :
        if args[1] in plugs['pluginlist'].pluginlist :
            try :
                connection.ircsend(info["channel"], plugs[args[1]].helpstring)
            except : connection.ircsend(info["channel"], "There is no help for that plugin")
            
