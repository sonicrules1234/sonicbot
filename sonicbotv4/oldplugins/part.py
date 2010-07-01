helpstring = "part <channel>"
minlevel = 4
arguments = ["self", "args"]
def main(connection, args) :
    """Parts from the specifed channel"""
    connection.rawsend("PART %s \n" % (args[1]))
