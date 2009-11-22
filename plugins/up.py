arguments = ["self", "info", "args"]
helpstring = "up"
needop = True

def main(connection, info, args) :
    connection.rawsend("MODE %s +o %s\n" % (info["channel"], info["sender"]))
