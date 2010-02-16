helpstring = "devoice <nick>"
arguments = ["self", "info", "args"]
minlevel = 3
def main(connection, info, args) :
    """Devoices a user"""
    connection.rawsend("MODE %s -v %s\n" % (info["channel"], args[1]))
