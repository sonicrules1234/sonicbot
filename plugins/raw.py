arguments = ["self", "info", "args"]
minlevel = 5
helpstring = "raw <rawstr>"
def main(connection, info, args) :
    connection.rawsend(" ".join(args[1:]) + "\n")
