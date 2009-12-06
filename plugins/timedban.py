arguments = ["self", "info", "args", "reactor"]
helpstring = "timedban <nick> <minutes>"
minlevel = 3
def main(connection, info, args, reactor) :
    if args[1] in connection.nicks.keys() :
        target = "*!*@%s" % (connection.nicks[args[1]])
    else : target = "%s*!*@*" % (args[1])
    connection.rawsend("MODE %s +b %s\n" % (info["channel"], target))
    reactor.callLater(int(args[2]) * 60, unban, [connection,"MODE %s +b %s\n" % (info["channel"], target)])
def unban(infolist) :
    infolist[0].rawsend(infolist[1])
