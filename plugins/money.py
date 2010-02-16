import shelve
arguments = ["self", "info", "args", "world"]
minlevel = 2
helpstring = "money [person]"

def main(connection, info, args, world) :
    """Returns amount of money"""
    money = shelve.open("money-%s.db" % (world.hostnicks[connection.host]), writeback=True)
    if len(args) == 1 :
        target = info["sender"]
    else : target = args[1]
    if money.has_key(target) :
        connection.ircsend(info["channel"], "%s has %s dollars." % (target, str(money[target]["money"])))
    else : connection.ircsend(info["channel"], "No such user %s in my database." % (target))
    
