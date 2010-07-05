arguments = ["self", "info", "args"]
minlevel = 4
helpstring = "raw <rawstr>"
def main(connection, info, args) :
    """Sends raw text"""
    connection.rawsend(" ".join(args[1:]) + "\n")
