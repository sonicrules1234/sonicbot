arguments = ["self", "info", "args", "conf"]
helpstring = "admin"
needop = False

def main(connection, info, args, conf) :
    connection.ircsend(info["channel"], "%s: The current %s admin are: %s" % (info["sender"], conf.nick, ", ".join(conf.admin)))
