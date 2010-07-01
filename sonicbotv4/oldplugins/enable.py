arguments = ["self", "info", "args"]
minlevel = 3
helpstring = "enable <plugin>"

def main(connection, info, args) :
    """Enables a plugin"""
    if args[1] not in ["disable", "enable", "*"] :
        if args[1] not in connection.users["channels"][info["channel"]]["enabled"] :
            connection.users["channels"][info["channel"]]["enabled"].append(args[1])
            connection.users.sync()
            connection.ircsend(info["channel"], _("The %(pluginname)s plugin has been enabled in this channel") % dict(pluginname=args[1]))
        else : connection.ircsend(info["channel"], _("That plugin is not disabled!"))
    elif args[1] in ["enable", "disable"] : connection.ircsend(info["channel"], _("You cannot enable the disable or enable commands!"))
    elif args[1] == "*" :
        for plugin in connection.plugins["pluginlist"].pluginlist :
            if plugin not in ["enable", "disable"] and plugin not in connection.users["channels"][info["channel"]]["enabled"]:
                connection.users["channels"][info["channel"]]["enabled"].append(plugin)
                connection.users.sync()
        connection.ircsend(info["channel"], _("All plugins have been enabled for this channel"))
