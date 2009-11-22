import random
arguments = ["self", "info", "args"]
needop = False
helpstring = "choose <choices seperated by ' or '>"

def main(connection, info, args) :
    choices = " ".join(args[1:]).split(" or ")
    chosen = random.choice(choices)
    connection.ircsend(info["channel"], "%s: I choose %s." % (info["sender"], chosen))
