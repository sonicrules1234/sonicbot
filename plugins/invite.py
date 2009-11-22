arguments = ["self", "info", "args"]
helpstring = "invite <nick>"
needop = True

def main(connection, info, args) :
    connection.rawsend("INVITE %s %s\n" % (args[1], info["channel"]))
