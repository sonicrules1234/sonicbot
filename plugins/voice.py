helpstring = "voice <nick>"
arguments = ["self", "info", "args"]
minlevel = 3
def main(connection, info, args) :
    for person in args[1:] :
        connection.rawsend("MODE %s +v %s\n" % (info["channel"], person))
