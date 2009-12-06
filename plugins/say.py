helpstring = "say <channel> <message>"
minlevel = 4
arguments = ["self", "args"]
def main(connection, args) :
    connection.ircsend(args[1], " ".join(args[2:]))
