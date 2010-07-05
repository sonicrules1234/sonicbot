helpstring = "ban <nick>"
arguments = ["self", "info", "args"]
minlevel = 3
def main(connection, info, args) :
    """Bans a user"""
    if args[1] in connection.hostnames.keys() :
        target = "*!*@%s" % (connection.hostnames[args[1]])
    else : target = "%s*!*@*" % (args[1])
    connection.rawsend("MODE %s +b %s\n" % (info["channel"], target))
