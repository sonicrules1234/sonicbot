helpstring = "error"
arguments = ["self", "info", "args"]
minlevel = 5

def main(connection, info, args) :
    connection.ircsend(info["sender"], connection.error)
