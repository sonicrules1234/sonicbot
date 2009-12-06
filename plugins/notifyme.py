import shelve
helpstring = "notifyme <nick>"
arguments = ["self", "info", "args"]
minlevel = 1

def main(connection, info, args) :
    args = [x.lower() for x in args]
    notify = shelve.open("notify.db", writeback=True)
    if args[1] not in notify.keys() :
        notify[args[1]] = []
        notify.sync()
    notify[args[1]].append(info["sender"].lower())
    notify.sync()
    notify.close()
    connection.ircsend(info["channel"], "%s: I will notify you when %s arrives or says something." % (info["sender"], args[1]))
    
