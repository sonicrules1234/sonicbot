import shelve
arguments = ["self", "info", "args", "world"]
minlevel = 2
helpstring = "money [person]"

def main(connection, info, args, world) :
    """Returns amount of money"""
    money = shelve.open("money-%s.db" % (connection.networkname), writeback=True)
    if len(args) == 1 :
        target = info["sender"]
    else : target = args[1]
    if money.has_key(target) :
        connection.msg(info["channel"], _("%(nick)s has %(num)s dollars.") % dict(nick=target, num=str(money[target]["money"])))
    else : connection.msg(info["channel"], _("No such user %(nick)s in my database.") % dict(nick=target))
    
