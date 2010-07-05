arguments = ["self", "info", "args"]
helpstring = "dance"
minlevel = 1

def main(connection, info, args) :
    """Sends a message that looks like somebody is dancing"""
    connection.notice(info["sender"], "\n".join([":D%s-<" % (x) for x in [y for y in "|/|\\|/|"]]))
    
