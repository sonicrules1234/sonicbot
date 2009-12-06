helpstring = "part <channel>"
minlevel = 4
arguments = ["self", "args"]
def main(connection, args) :
    connection.rawsend("PART %s \n" % (args[1]))
