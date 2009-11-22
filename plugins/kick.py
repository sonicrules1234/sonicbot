helpstring = "kick <nick>"
arguments = ["self", "info", "args", "conf"]
needop = True
def main(connection, info, args, conf) :
    connection.rawsend("KICK %s %s :%s\n" % (info["channel"], args[1], " ".join(args[2:])))
