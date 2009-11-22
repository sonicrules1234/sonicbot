arguments = ["self", "info", "args"]
needop = True
helpstring = "action <channel> <action>"
def main(connection, info, args) :
    connection.ircsend(args[1], "\x01ACTION %s\x01" % (" ".join(args[2:])))
