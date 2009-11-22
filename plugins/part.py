helpstring = "part <channel>"
needop = True
arguments = ["self", "args"]
def main(connection, args) :
    connection.rawsend("PART %s \n" % (args[1]))
