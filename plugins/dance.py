arguments = ["self", "info", "args"]
helpstring = "dance"
minlevel = 1

def main(connection, info, args) :
    connection.ircsend(info["sender"], "\n".join([":D%s-<" % (x) for x in [y for y in "|/|\\|/|"]]))
    
