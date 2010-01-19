import base64
helpstring = "b64 encode|decode <string>"
minlevel = 1
arguments = ["self", "info", "args"]

def main(connection, info, args) :
    if args[1] == "encode" :
        connection.ircsend(info["channel"], "%s: %s" % (info["sender"], base64.b64encode(" ".join(args[2:]))))
    elif args[1] == "decode" :
        connection.ircsend(info["channel"], "%s: %s" % (info["sender"], base64.b64decode(args[2])))
