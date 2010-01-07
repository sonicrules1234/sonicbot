minlevel = 1
helpstring = "minlevel <command>"
arguments = ["self", "info", "args", "self.plugins"]

def main(connection, info, args, plugins) :
    if args[1] in plugins["pluginlist"].pluginlist :
        connection.ircsend(info["channel"], "The minimum user level needed for that plugin is: %s." % (plugins[args[1]].minlevel))
    else : connection.ircsend(info["channel"], "No such plugin.")
