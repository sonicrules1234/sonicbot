arguments = ["self", "info", "args"]
minlevel = 3
helpstring = "mode [nick]"

def main(connection, info, args) :
    """Changes modes on a nick/channel"""
    connection.rawsend("MODE %s %s\n" % (info["channel"], " ".join(args[1:])))
