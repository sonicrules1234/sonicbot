arguments = ["self", "info", "args"]
helpstring = "dance"
needop = False

def main(connection, info, args) :
    connection.ircsend(info["sender"], "\n".join([":D%s-<" % (x) for x in [y for y in "|/|\\|/|"]]))
    
