import shelve, time, random
def main(connection, info, conf) :
    args = info["message"].replace("\x01", "").split(" ")[1:]
    contextdb = shelve.open("context.db", writeback=True)
    if not contextdb.has_key(info["channel"]) and info["channel"].startswith("#") :
        contextdb[info["channel"]] = ["<%s> %s" % (info["sender"], info["message"])]
        contextdb.sync()
    elif contextdb.has_key(info["channel"]) :
        contextdb[info["channel"]].append("*%s %s" % (info["sender"], " ".join(args).replace("", "")))
        contextdb.sync()
        if len(contextdb[info["channel"]]) > 10 :
            contextdb[info["channel"]].pop(0)
            contextdb.sync()
    contextdb.close()
    seendb = shelve.open("seen.db", writeback=True)
    if not seendb.has_key("users") :
        seendb["users"] = {}
        seendb.sync()
    seendb["users"][info["sender"].lower()] = [time.time(), "*%s %s" % (info["sender"], " ".join(args).replace("", ""))]
    seendb.close()
    if args[0] in ["slaps", "punches", "stomps", "hurts", "rapes", "hits", "fucks", "smacks", "crunches", "kicks", "barfs", "forces", "force", "squishes", "bodyslams", "shoots", "compresses", "tackles"] :
        if args[1] == conf.nick or args[-1] == conf.nick :
            connection.ircsend(info["channel"], random.choice(["Oww!", "Ouch, that hurt!", "\x01ACTION curls up in fetal position\x01", "\x01ACTION slaps %s\x01" % (info["sender"]), "\x01ACTION smacks %s\x01" % (info["sender"]), "\x01ACTION kicks %s\x01" % (info["sender"])]))
            
