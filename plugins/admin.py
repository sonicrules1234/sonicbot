arguments = ["self", "info", "args", "conf"]
helpstring = "admin"
minlevel = 1

def main(connection, info, args, conf) :
    """Displays the admins from the config"""
    connection.ircsend(info["channel"], "%s: The current %s admin are: %s" % (info["sender"], conf.nick, ", ".join(conf.admin)))
