helpstring = "say <channel> <message>"
minlevel = 4
arguments = ["self", "args"]
def main(connection, args) :
    """Makes sonicbot say something in the specified channel"""
    connection.ircsend(args[1], " ".join(args[2:]))
