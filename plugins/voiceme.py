helpstring = "voiceme"
arguments = ["self", "info", "args"]
needop = False
def main(connection, info, args) :
    connection.rawsend("MODE %s +v %s\n" % (info["channel"], info["sender"]))
