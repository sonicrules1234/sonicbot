arguments = ["self", "info", "args"]
needop = True
helpstring = "raw <rawstr>"
def main(connection, info, args) :
    connection.rawsend(" ".join(args[1:]) + "\n")
