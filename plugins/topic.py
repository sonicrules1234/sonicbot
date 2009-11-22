arguments = ["self", "info", "args"]
helpstring = "topic <topic>"
needop = True
def main(connection, info, args) :
    connection.rawsend("TOPIC %s :%s\n" % (info["channel"], " ".join(args[1:])))
