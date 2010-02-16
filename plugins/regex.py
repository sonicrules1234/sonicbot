import re
arguments = ["self", "info", "args"]
helpstring = "regex <pattern> <string>"
minlevel = 1

def main(connection, info, args) :
    """Evaluates regex"""
    connection.ircsend(info["channel"], repr(re.search(args[1], args[2]).groups()))
