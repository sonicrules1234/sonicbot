helpstring = "ban <nick>"
arguments = ["self", "info", "args"]
needop = True
def main(connection, info, args) :
    if args[1] in connection.nicks.keys() :
        target = "*!*@%s" % (connection.nicks[args[1]])
    else : target = "%s*!*@*" % (args[1])
    connection.rawsend("MODE %s +b %s\n" % (info["channel"], target))
