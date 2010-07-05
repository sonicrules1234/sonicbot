arguments = ["self", "info", "args"]
helpstring = "cycle"
minlevel = 3

def main(connection, info, args) :
    """Cycles the channel"""
    connection.rawsend("PART %s\nJOIN %s\n" % (info['channel'], info['channel']))
