import shelve
arguments = ["self", "info", "args", "world"]
minlevel = 2
helpstring = "money [person]"

def main(connection, info, args, world) :
    money = shelve.open("money-%s.db" % (world.hostnicks[connection.host]), writeback=True)
    if len(args) == 1 :
        target = info["sender"]
    if money.has_key(target) :
        connection.ircsend(info["channel"], "%s has %s dollars." % (target))
    else : connection.ircsend(info["channel"], "No such user %s in my database." % (target))
    
