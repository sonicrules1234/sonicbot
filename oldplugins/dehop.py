arguments = ["self", "info", "args", "conf"]
minlevel = 3
helpstring = "dehop [nick]"

def main(connection, info, args, conf) :
    """De-half-ops a user"""
    if len(args) == 1 : target = info["sender"]
    else : target = args[1]
    connection.rawsend("MODE %s -h %s\n" % (info["channel"], target))
    if info["channel"] in conf.avchans :
        connection.rawsend("MODE %s +v %s\n" % (info["channel"], target))
