minlevel = 1
helpstring = "minlevel <command>"
arguments = ["self", "info", "args", "self.plugins"]

def main(connection, info, args, plugins) :
    """Returns the minimum user level for a plugin"""
    if args[1] in plugins["pluginlist"].pluginlist :
        connection.msg(info["channel"], _("The minimum user level needed for that plugin is: %(level)s.") % dict(level=plugins[args[1]].minlevel))
    else : connection.msg(info["channel"], _("No such plugin."))
