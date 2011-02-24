minlevel = 1
helpstring = "minlevel <command>"
arguments = ["self", "info", "args", "world"]

def main(connection, info, args, plugins) :
    """Returns the minimum user level for a plugin"""
    if world.plugins.has_key(args[1]) :
        connection.msg(info["channel"], _("The minimum user level needed for that plugin is: %(level)s.") % dict(level=world.plugins[args[1]]["minlevel"]))
    else : connection.msg(info["channel"], _("No such plugin."))
