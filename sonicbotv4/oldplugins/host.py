arguments = ["self", "info", "args"]
helpstring = "host <nick>"
minlevel = 1

def main(connection, info, args) :
    """Specifies the hostname of the nick given"""
    connection.msg(info["channel"], '%s: "%s"' % (info["sender"], connection.hostnames[args[1]]))
