arguments = ["self", "info", "args"]
helpstring = "cycle"
needop = True

def main(connection, info, args) :
    connection.rawsend("PART %s\nJOIN %s\n" % (info['channel'], info['channel']))
