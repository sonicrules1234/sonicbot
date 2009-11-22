arguments = ["self", "info", "args"]
helpstring = "lurk"
needop = True

def main(connection, info, args) :
    connection.rawsend("MODE %s -o %s\n" % (info["channel"], info["sender"]))
    connection.rawsend("MODE %s +v %s\n" % (info["channel"], info["sender"]))
