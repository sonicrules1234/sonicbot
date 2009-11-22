helpstring = "say <channel> <message>"
needop = True
arguments = ["self", "args"]
def main(connection, args) :
    connection.ircsend(args[1], " ".join(args[2:]))
