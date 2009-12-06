arguments = ["self", "info", "args"]
minlevel = 3
helpstring = "hop [nick]"

def main(connection, info, args) :
    if len(args) == 1 : target = info["sender"]
    else : target = args[1]
    connection.rawsend("MODE %s +h %s\n" % (info["channel"], target))
