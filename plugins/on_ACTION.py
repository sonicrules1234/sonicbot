import shelve, time, random
def main(connection, info, conf) :
    """Runs every time somebody does an action (/me)"""
    badwords = shelve.open("badwords.db", writeback=True)
    if badwords.has_key(connection.host) :
        if badwords[connection.host].has_key(info["channel"]) :
            nosay = badwords[connection.host][info["channel"]]["badwords"]
            for word in nosay :
                if word in info["message"].lower().replace(" ", "") :
                    if info["sender"] not in badwords[connection.host][info["channel"]]["users"] :
                        badwords[connection.host][info["channel"]]["users"][info["sender"]] = 0
                        badwords.sync()
                    if badwords[connection.host][info["channel"]]["users"][info["sender"]] > 0 :
                        if info["sender"] in connection.nicks.keys() :
                            target = "*!*@%s" % (connection.nicks[info["sender"]])
                        else : target = "%s*!*@*" % (info["sender"])
                        connection.rawsend("MODE %s +b %s\n" % (info["channel"], target))
                    connection.rawsend("KICK %s %s :%s\n" % (info["channel"], info["sender"], "Don't use that word!"))
                    badwords[connection.host][info["channel"]]["users"][info["sender"]] += 1
                    badwords.sync()
    badwords.close()
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
    if len(args) > 1 :
        if args[0] in ["slaps", "punches", "stomps", "hurts", "rapes", "hits", "fucks", "smacks", "crunches", "kicks", "barfs", "forces", "force", "squishes", "bodyslams", "shoots", "compresses", "tackles"] :
            if args[1] == conf.nick or args[-1] == conf.nick :
                connection.ircsend(info["channel"], random.choice(["Oww!", "Ouch, that hurt!", "\x01ACTION curls up in fetal position\x01", "\x01ACTION slaps %s\x01" % (info["sender"]), "\x01ACTION smacks %s\x01" % (info["sender"]), "\x01ACTION kicks %s\x01" % (info["sender"]), "\x01ACTION explodes\x01"]))
                
