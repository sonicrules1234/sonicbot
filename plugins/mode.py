arguments = ["self", "info", "args"]
needop = True
helpstring = "mode [nick]"

def main(connection, info, args) :
    connection.rawsend("MODE %s %s\n" % (info["channel"], " ".join(args[1:])))
