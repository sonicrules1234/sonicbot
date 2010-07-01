arguments = ["self", "info", "args"]
minlevel = 4
helpstring = "join <channel>"
def main(connection, info, args):
    """Makes sonicbot join a channel"""
    connection.rawsend("JOIN %s\n" % (args[1]))
