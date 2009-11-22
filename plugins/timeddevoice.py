arguments = ["self", "info", "args", "reactor"]
helpstring = "timeddevoice <nick> <minutes>"
needop = True
def main(connection, info, args, reactor) :
    connection.rawsend("MODE %s -v %s\r\n" % (info["channel"], args[1]))
    reactor.callLater(int(args[2]) * 60, devoice, [connection, info, args[1]])
def devoice(infolist) :
    infolist[0].rawsend("MODE %s +v %s\r\n" % (infolist[1]["channel"], infolist[2]))
