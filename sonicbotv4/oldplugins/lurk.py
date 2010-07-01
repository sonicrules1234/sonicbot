arguments = ["self", "info", "args"]
helpstring = "lurk"
minlevel = 3

def main(connection, info, args) :
    """Deops and voices the sender"""
    connection.rawsend("MODE %s -o %s\n" % (info["channel"], info["sender"]))
    connection.rawsend("MODE %s +v %s\n" % (info["channel"], info["sender"]))
