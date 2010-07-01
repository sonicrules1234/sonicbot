import random
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "choose <choices seperated by ' or '>"

def main(connection, info, args) :
    """Makes a choice from given choices"""
    choices = " ".join(args[1:]).split(" or ")
    chosen = random.choice(choices)
    connection.msg(info["channel"], _("%(sender)s: I choose %(choice)s.") % dict(sender=info["sender"], choice=chosen))
