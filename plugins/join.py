arguments = ["self", "info", "args"]
minlevel = 4
helpstring = "join <channel>"
def main(connection, info, args):
    connection.rawsend("JOIN %s\n" % (args[1]))
