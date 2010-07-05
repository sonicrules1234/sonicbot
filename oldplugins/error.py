helpstring = "error"
arguments = ["self", "info", "args"]
minlevel = 5

def main(connection, info, args) :
    """Returns the traceback for the last error"""
    connection.notice(info["sender"], connection.error)
