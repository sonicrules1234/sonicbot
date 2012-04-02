import shelve, time
arguments = ["self", "info", "args"]
helpstring = "memo <nick> <message>"
minlevel = 1

def main(connection, info, args) :
    """Has the bot tell the specified nick the message when they are seen"""
    db = shelve.open("memos.db", writeback=True)
    if not db.has_key(args[1].lower()) :
        db[args[1].lower()] = []
        db.sync()
    if len(db[args[1]].lower()) < 3 :
        if len(db[args[1].lower()]) > 0 :
            if " ".join(args[2:]) == db[args[1].lower()][-1]["message"] and info["sender"] == db[args[1].lower()][-1]["sender"] :
                connection.ircsend(info["channel"], "%(sender)s: Ignoring repeated message." % dict(sender=info["sender"]))
        else :
            db[args[1].lower()].append({"sender":info["sender"], "message":" ".join(args[2:]), "time":time.time()})
            db.sync()
            db.close()
            connection.ircsend(info["channel"], "%(sender)s: Message sent." % dict(sender=info["sender"]))
    else : connection.ircsend(info["channel"], "Sorry, but that person already has 3 memos.")
