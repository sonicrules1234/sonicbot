import shelve
def main(connection, info, conf) :
    args = info["message"].split(" ")[1:]
    contextdb = shelve.open("context.db", writeback=True)
    if not contextdb.has_key(info["channel"]) and info["channel"].startswith("#") :
        contextdb[info["channel"]] = ["<%s> %s" % (info["sender"], info["message"])]
        contextdb.sync()
    elif contextdb.has_key(info["channel"]) :
        contextdb[info["channel"]].append("*%s %s" % (info["sender"], " ".join(args[1:]).replace("", "")))
        contextdb.sync()
        if len(contextdb[info["channel"]]) > 10 :
            contextdb[info["channel"]].pop(0)
            contextdb.sync()
    contextdb.close()
    seendb = shelve.open("seen.db", writeback=True)
    if not seendb.has_key("users") :
        seendb["users"] = {}
        seendb.sync()
    seendb["users"][info["sender"].lower()] = [time.time(), "*%s %s" % (info["sender"], " ".join(args[1:]).replace("", ""))]
    seendb.close()
