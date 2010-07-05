import shelve, time
arguments = ["self", "info", "args"]
helpstring = "memo <nick> <message>"
minlevel = 1

def main(connection, info, args) :
    db = shelve.open("memos.db", writeback=True)
    if not db.has_key(info["sender"].lower()) :
        db[info["sender"].lower()] = []
        db.sync()
    db[info["sender"].lower()].append({"sender":info["sender"], "message":" ".join(args[2:]), "time":time.time()})
    db.sync()
    db.close()
    connection.ircsend(info["channel"], "%(sender)s: Message sent." % dict(sender=info["sender"]))