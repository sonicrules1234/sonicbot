arguments = ["self", "info", "args"]
helpstring = "lurk"
minlevel = 3

def main(connection, info, args) :
    """Deops and voices the sender"""
    connection.rawsend("MODE %s -o+v %s %s\n" % (info["channel"], info["sender"], info["sender"]))
