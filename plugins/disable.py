arguments = ["self", "info", "args"]
minlevel = 3
helpstring = "disable <plugin>"

def main(connection, info, args) :
    """Disables a plugin"""
    if args[1] not in ["disable", "enable", "*"] :
        if args[1] in connection.users["channels"][info["channel"]]["enabled"] :
            connection.users["channels"][info["channel"]]["enabled"].remove(args[1])
            connection.users.sync()
            connection.ircsend(info["channel"], "The %s plugin has been disabled in this channel" % (args[1]))
        else : connection.ircsend(info["channel"], "That plugin is not enabled!")
    elif args[1] in ["enable", "disable"] : connection.ircsend(info["channel"], "You cannot disable the disable or enable commands!")
    elif args[1] == "*" :
        for plugin in connection.plugins["pluginlist"].pluginlist :
            if plugin not in ["enable", "disable"] and plugin in connection.users["channels"][info["channel"]]["enabled"]:
                connection.users["channels"][info["channel"]]["enabled"].remove(plugin)
                connection.users.sync()
                print plugin
        connection.ircsend(info["channel"], "All plugins have been disabled for this channel")
