import base64
helpstring = "b64 encode|decode <string>"
minlevel = 1
arguments = ["self", "info", "args"]

def main(connection, info, args) :
    """Decodes/encodes using base64"""
    if args[1] == "encode" :
        connection.msg(info["channel"], "%s: %s" % (info["sender"], base64.b64encode(" ".join(args[2:]))))
    elif args[1] == "decode" :
        connection.msg(info["channel"], "%s: %s" % (info["sender"], base64.b64decode(args[2]).replace("\n", "").replace("\r", "")))
