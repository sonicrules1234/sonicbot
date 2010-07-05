import shelve
helpstring = "notifyme <nick>"
arguments = ["self", "info", "args"]
minlevel = 1

def main(connection, info, args) :
    """Stores data to notify the sender when the specified nick does something"""
    args = [x.lower() for x in args]
    notify = shelve.open("notify.db", writeback=True)
    if args[1] not in notify.keys() :
        notify[args[1]] = []
        notify.sync()
    notify[args[1]].append(info["sender"].lower())
    notify.sync()
    notify.close()
    connection.msg(info["channel"], _("%(sender)s: I will notify you when %(nick)s arrives or says something.") % dict(sender=info["sender"], nick=args[1]))
    
