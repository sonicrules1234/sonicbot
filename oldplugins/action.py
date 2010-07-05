arguments = ["self", "info", "args"]
minlevel = 4
helpstring = "action <channel> <action>"
def main(connection, info, args) :
    """Does an action, ie /me"""
    connection.msg(args[1], "\x01ACTION %s\x01" % (" ".join(args[2:])))
