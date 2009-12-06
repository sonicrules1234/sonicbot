helpstring = "voiceme"
arguments = ["self", "info", "args"]
minlevel = 3
def main(connection, info, args) :
    connection.rawsend("MODE %s +v %s\n" % (info["channel"], info["sender"]))
