helpstring = "devoice <nick>"
arguments = ["self", "info", "args"]
needop = True
def main(connection, info, args) :
    connection.rawsend("MODE %s -v %s\n" % (info["channel"], args[1]))
