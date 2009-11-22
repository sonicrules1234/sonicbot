arguments = ["self", "info", "args"]
helpstring = "host <nick>"
needop = False

def main(connection, info, args) :
    connection.ircsend(info["channel"], '%s: "%s"' % (info["sender"], connection.nicks[args[1]]))
