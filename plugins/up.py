arguments = ["self", "info", "args"]
helpstring = "up"
minlevel = 3

def main(connection, info, args) :
    connection.rawsend("MODE %s +o %s\n" % (info["channel"], info["sender"]))
