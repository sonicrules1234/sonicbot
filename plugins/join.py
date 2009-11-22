arguments = ["self", "info", "args"]
needop = True
helpstring = "join <channel>"
def main(connection, info, args):
    connection.rawsend("JOIN %s\n" % (args[1]))
