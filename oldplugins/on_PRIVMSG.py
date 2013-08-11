import shelve, time, random
def main(connection, info) :
    """This is the old plugin"""
#"""Run every time a message is seen"""
    if info["message"].startswith("\x01ACTION") and info["message"].endswith("\x01") :
        on_ACTION(connection, info)
        return None
#    if info["sender"] == "OperServ" :
#        words = info["message"].split(" ")
#        if words[0] == "REGISTER:" :
#            newchannel = words[1].replace("\002", "")
#            registeree = words[3].replace("\002", "")
#            connection.rawsend("JOIN %s\n" % (newchannel))
#            connection.rawsend("MODE %s +o %s\n" % (newchannel, conf.nick))
#            connection.msg(newchannel, "Hello %s, I am sonicbot and I am here to help you with IRC." % (registeree))
    seendb = shelve.open("seen.db", writeback=True)
    if not seendb.has_key("users") :
        seendb["users"] = {}
        seendb.sync()
    seendb["users"][info["sender"].lower()] = [time.time(), info["message"]]
    seendb.sync()
    seendb.close()
    badwords = shelve.open("badwords.db", writeback=True)
    if badwords.has_key(connection.host) :
        if badwords[connection.host].has_key(info["channel"]) :
            nosay = badwords[connection.host][info["channel"]]["badwords"]
            for word in nosay :
                if word in [message.replace(".", "").replace("!","").replace("?", "") for message in info["message"].lower().split(" ")] :
                    if info["sender"] not in badwords[connection.host][info["channel"]]["users"] :
                        badwords[connection.host][info["channel"]]["users"][info["sender"]] = 0
                        badwords.sync()
#                    if badwords[connection.host][info["channel"]]["users"][info["sender"]] > 0 :
#                        if info["sender"] in connection.hostnames.keys() :
#                            target = "*!*@%s" % (connection.hostnames[info["sender"]])
#                        else : target = "%s*!*@*" % (info["sender"])
#                        connection.rawsend("MODE %s +b %s\n" % (info["channel"], target))
                    connection.rawsend("KICK %s %s :%s (%s)\n" % (info["channel"], info["sender"], "Don't use that word!", word))
                    badwords[connection.host][info["channel"]]["users"][info["sender"]] += 1
                    badwords.sync()
    badwords.close()
    if info["sender"] not in connection.ignorelist :
        if info["message"].lower().startswith("hi") or info["message"].lower().startswith("hello") or info["message"].lower().startswith("hey") :
            if connection.nick.lower() in info["message"].lower() :
                connection.msg(info["channel"], _("Hello %(sender)s!") % dict(sender=info["sender"]))
    contextdb = shelve.open("context.db", writeback=True)
    if not contextdb.has_key(info["channel"]) and info["channel"].startswith("#") :
        contextdb[info["channel"]] = ["<%s> %s" % (info["sender"], info["message"])]
        contextdb.sync()
    elif contextdb.has_key(info["channel"]) :
        contextdb[info["channel"]].append("<%s> %s" % (info["sender"], info["message"]))
        contextdb.sync()
        if len(contextdb[info["channel"]]) > 10 :
            contextdb[info["channel"]].pop(0)
            contextdb.sync()
    contextdb.close()
    memos = shelve.open("memos.db", writeback=True)
    if memos.has_key(info["sender"].lower()) :
        for memo in memos[info["sender"].lower()] :
            connection.ircsend(info["channel"], "%(sender)s: %(memoer)s sent you a memo! '%(memo)s'" % {"sender":info["sender"], "memoer":memo["sender"], "memo":memo["message"]})
        memos[info["sender"].lower()] = []
        memos.sync()
    memos.close()
    


#    if info["sender"] not in conf.ignorelist and info["hostname"] not in conf.hostignores :
#        combos = shelve.open("combos.db", writeback=True)
#        if info["channel"] not in combos.keys() :
#            combos[info["channel"]] = []
#            combos.sync()
#        combos[info["channel"]].append(info["message"])
#        combos.sync()
#        if len(combos[info["channel"]]) > 3 :
#            combos[info["channel"]].pop(0)
#            combos.sync()
#        if len(combos[info["channel"]]) == 3 :
#            temp = combos[info["channel"]]
#            if temp[1].lower().startswith(temp[0].lower()) and temp[2].lower().startswith(temp[0].lower()) :
#                connection.msg(info["channel"], temp[0])
#                del combos[info["channel"]]
#                combos.sync()
#        combos.close()

    if info["message"].startswith("PING") : connection.notice(info["sender"], info["message"])
    mail = shelve.open("mail.db", writeback=True)
    if info["sender"].replace("[", "").replace("]", "") in mail.keys() :
        if info["hostname"] in mail[info["sender"].replace("[", "").replace("]", "")]["hostname"] :
            if mail[info["sender"].replace("[", "").replace("]", "")]["notify"] :
                connection.msg(info["sender"], _("You have new mail."))
                mail[info["sender"].replace("[", "").replace("]", "")]["notify"] = False
                mail.sync()
    mail.close()
    emotions = shelve.open("emotions.db", writeback=True)
    info["sender"] = info["sender"].lower()
    if info["sender"].lower() not in emotions.keys() and happiness_detect(info) :
        emotions[info["sender"].lower()] = {}
        emotions.sync()
        emotions[info["sender"].lower()]["happy"] = 0
        emotions.sync()
        emotions[info["sender"].lower()]["sad"] = 0
        emotions.sync()
    if info["sender"].lower() in emotions.keys() :
        for emotion in [":)", ":D", "C:", "=D", ";p", "=)", "C=", "(=", "(:" "xD", "=p", ":p"] :
            if emotion in info["message"] :
                emotions[info["sender"].lower()]["happy"] += 1
                emotions.sync()
                break
        for emotion in [":(", "D:", "=(", "D=", "):", ")=", "=C", ":C"] :
            if emotion in info["message"] :
                emotions[info["sender"].lower()]["sad"] += 1
                emotions.sync()
                break
        if ":P" in info["message"] :
            emotions[info["sender"].lower()]["happy"] += .5
            emotions.sync()
    emotions.close()
    notify = shelve.open("notify.db", writeback=True)
    if info["sender"] in notify.keys() :
        temp = notify[info["sender"]]
        for user in temp :
            connection.msg(user, _("%(nick)s has just said something in %(channel)s") % dict(nick=info["sender"], channel=info["channel"]))
            notify[info["sender"]].remove(user)
            notify.sync()
        if notify[info["sender"]] == [] :
            del notify[info["sender"]]
            notify.sync()
    notify.close()

def happiness_detect(info) :
    """Checks to see if a smiley is in the message"""
    for emotion in [":)", ":D", "C:", "=D", "=)", "C=", "(=", "(:" "xD", ":p", ";p", "=p", ":(", "D:", "=(", "D=", "):", ")=", "=C", ":C", ":P"] :
        if emotion in info["message"] : return True
    return False
def on_ACTION(connection, info) :
    """Runs every time somebody does an action (/me)"""
    badwords = shelve.open("badwords.db", writeback=True)
    if badwords.has_key(connection.host) :
        if badwords[connection.host].has_key(info["channel"]) :
            nosay = badwords[connection.host][info["channel"]]["badwords"]
            for word in nosay :
                if word in [message.replace(".", "").replace("!","").replace("?", "") for message in info["message"].lower().split(" ")] :
                    if info["sender"] not in badwords[connection.host][info["channel"]]["users"] :
                        badwords[connection.host][info["channel"]]["users"][info["sender"]] = 0
                        badwords.sync()
#                    if badwords[connection.host][info["channel"]]["users"][info["sender"]] > 0 :
#                        if info["sender"] in connection.hostnames.keys() :
#                            target = "*!*@%s" % (connection.hostnames[info["sender"]])
#                        else : target = "%s*!*@*" % (info["sender"])
#                        connection.rawsend("MODE %s +b %s\n" % (info["channel"], target))
                    connection.rawsend("KICK %s %s :%s (%s)\n" % (info["channel"], info["sender"], "Don't use that word!", word))
                    badwords[connection.host][info["channel"]]["users"][info["sender"]] += 1
                    badwords.sync()
    badwords.close()
    memos = shelve.open("memos.db", writeback=True)
    if memos.has_key(info["sender"].lower()) :
        for memo in memos[info["sender"].lower()] :
            connection.ircsend(info["channel"], "%(sender)s: %(memoer)s sent you a memo! '%(memo)s'" % {"sender":info["sender"], "memoer":memo["sender"], "memo":memo["message"]})
        memos[info["sender"].lower()] = []
        memos.sync()
    memos.close()

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
        if args[0] in ["slaps", "punches", "stomps", "hurts", "rapes", "hits", "fucks", "smacks", "crunches", "kicks", "barfs", "forces", "force", "squishes", "bodyslams", "shoots", "compresses", "tackles", "stabs"] :
            if args[1] == connection.nick or args[-1] == connection.nick :
                connection.msg(info["channel"], random.choice(["Oww!", "Ouch, that hurt!", "\x01ACTION curls up in fetal position\x01", "\x01ACTION slaps %s\x01" % (info["sender"]), "\x01ACTION smacks %s\x01" % (info["sender"]), "\x01ACTION kicks %s\x01" % (info["sender"]), "\x01ACTION explodes\x01"]))
    if len(args) > 1 :
        if args[0].lower() == "hugs" and args[1] == connection.nick :
            connection.msg(info["channel"], "\x01ACTION hugs %(sender)s\x01" % dict(sender=info["sender"]))

