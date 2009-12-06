arguments = ["self", "info", "args"]
helpstring = "host <nick>"
minlevel = 1

def main(connection, info, args) :
    connection.ircsend(info["channel"], '%s: "%s"' % (info["sender"], connection.nicks[args[1]]))
