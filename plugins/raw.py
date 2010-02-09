arguments = ["self", "info", "args"]
minlevel = 4
helpstring = "raw <rawstr>"
def main(connection, info, args) :
    connection.rawsend(" ".join(args[1:]) + "\n")
