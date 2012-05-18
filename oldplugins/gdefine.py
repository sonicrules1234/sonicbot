import gdefinelib
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "gdefine <phrase>"

def main(connection, info, args) :
    """Defines a word or phrase using google"""
    definition = gdefinelib.gdefine(args[1])
    message = definition[0] + ": " + definition[1]
    connection.msg(info["channel"], "%s: %s" % (info["sender"], message))
