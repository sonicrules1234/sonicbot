arguments = ["self", "info", "args"]
helpstring = "topic <topic>"
minlevel = 3
def main(connection, info, args) :
    """Changes the topic"""
    connection.rawsend("TOPIC %s :%s\n" % (info["channel"], " ".join(args[1:])))
