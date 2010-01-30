import re
arguments = ["self", "info", "args"]
helpstring = "regex <pattern> <string>"
minlevel = 1

def main(connection, info, args) :
    connection.ircsend(info["channel"], repr(re.search(args[1], args[2])))
