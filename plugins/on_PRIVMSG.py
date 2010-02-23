import shelve, time
# That import shelve tells me that you might be storing messages you get
# in that shelve and using it to write to the log file. Does that sound
# like something you might be doing sonic?
#
# ok, the problem with a python shelve, from my understanding of it
# is... this the shelve while being useful for writing logs also keeps the
# entire thing its writing a log of in memory as well. They are usually
# used for storing data to a file, and then re-reading that data in later.
def main(connection, info, conf) :
    """Run every time a message is seen"""
    if info["sender"] == "OperServ" :
        words = info["message"].split(" ")
        if words[0] == "REGISTER:" :
            newchannel = words[1].replace("\002", "")
            registeree = words[3].replace("\002", "")
            connection.rawsend("JOIN %s\n" % (newchannel))
            connection.rawsend("MODE %s +o %s\n" % (newchannel, conf.nick))
            connection.ircsend(newchannel, "Hello %s, I am sonicbot and I am here to help you with IRC." % (registeree))
    # seendb = shelve.open("seen.db", writeback=True)
    # if not seendb.has_key("users") :
    #     seendb["users"] = {}
    #     seendb.sync()
    # seendb["users"][info["sender"].lower()] = [time.time(), info["message"]]
    # seendb.sync()
    # seendb.close()
    # badwords = shelve.open("badwords.db", writeback=True)
    # if badwords.has_key(connection.host) :
    #     if badwords[connection.host].has_key(info["channel"]) :
    #         nosay = badwords[connection.host][info["channel"]]["badwords"]
    #         for word in nosay :
    #             if word in info["message"].lower().replace(" ", "") :
    #                 if info["sender"] not in badwords[connection.host][info["channel"]]["users"] :
    #                     badwords[connection.host][info["channel"]]["users"][info["sender"]] = 0
    #                     badwords.sync()
    #                 if badwords[connection.host][info["channel"]]["users"][info["sender"]] > 0 :
    #                     if info["sender"] in connection.nicks.keys() :
    #                         target = "*!*@%s" % (connection.nicks[info["sender"]])
    #                     else : target = "%s*!*@*" % (info["sender"])
    #                     connection.rawsend("MODE %s +b %s\n" % (info["channel"], target))
    #                 connection.rawsend("KICK %s %s :%s\n" % (info["channel"], info["sender"], "Don't use that word!"))
    #                 badwords[connection.host][info["channel"]]["users"][info["sender"]] += 1
    #                 badwords.sync()
    # badwords.close()
    if info["sender"] not in conf.ignorelist :
        if info["message"].lower().startswith("hi") or info["message"].lower().startswith("hello") or info["message"].lower().startswith("hey") :
            if conf.nick in info["message"].lower() :
                connection.ircsend(info["channel"], "Hello %s!" % (info["sender"]))
    # contextdb = shelve.open("context.db", writeback=True)
    # if not contextdb.has_key(info["channel"]) and info["channel"].startswith("#") :
    #     contextdb[info["channel"]] = ["<%s> %s" % (info["sender"], info["message"])]
    #     contextdb.sync()
    # elif contextdb.has_key(info["channel"]) :
    #     contextdb[info["channel"]].append("<%s> %s" % (info["sender"], info["message"]))
    #     contextdb.sync()
    #     if len(contextdb[info["channel"]]) > 10 :
    #         contextdb[info["channel"]].pop(0)
    #         contextdb.sync()
    # contextdb.close()
    


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
#                connection.ircsend(info["channel"], temp[0])
#                del combos[info["channel"]]
#                combos.sync()
#        combos.close()

    # if info["message"].startswith("PING") : connection.ircsend(info["sender"], info["message"])
    # mail = shelve.open("mail.db", writeback=True)
    # if info["sender"].replace("[", "").replace("]", "") in mail.keys() :
    #     if info["hostname"] in mail[info["sender"].replace("[", "").replace("]", "")]["hostname"] :
    #         if mail[info["sender"].replace("[", "").replace("]", "")]["notify"] :
    #             connection.ircsend(info["sender"], "You have new mail.")
    #             mail[info["sender"].replace("[", "").replace("]", "")]["notify"] = False
    #             mail.sync()
    # mail.close()
    # emotions = shelve.open("emotions.db", writeback=True)
    # info["sender"] = info["sender"].lower()
    # if info["sender"].lower() not in emotions.keys() and happiness_detect(info) :
    #     emotions[info["sender"].lower()] = {}
    #     emotions.sync()
    #     emotions[info["sender"].lower()]["happy"] = 0
    #     emotions.sync()
    #     emotions[info["sender"].lower()]["sad"] = 0
    #     emotions.sync()
    # if info["sender"].lower() in emotions.keys() :
    #     for emotion in [":)", ":D", "C:", "=D", ";p", "=)", "C=", "(=", "(:" "xD", "=p", ":p"] :
    #         if emotion in info["message"] :
    #             emotions[info["sender"].lower()]["happy"] += 1
    #             emotions.sync()
    #             break
    #     for emotion in [":(", "D:", "=(", "D=", "):", ")=", "=C", ":C"] :
    #         if emotion in info["message"] :
    #             emotions[info["sender"].lower()]["sad"] += 1
    #             emotions.sync()
    #             break
    #     if ":P" in info["message"] :
    #         emotions[info["sender"].lower()]["happy"] += .5
    #         emotions.sync()
    # emotions.close()

    ### Disable the notify part, including the shelve portion in the hope
    ### that shelve itself is the cause of our memoryleaks. If it is, then
    ### memory won't increase when we flood it under these settings. If it
    ### is not, memory will increase to 1.2 as in prior testing.
    if info["sender"] == "nixeagle" :
    connection.ircsend(info["sender"], "Hi nixeagle!")
    #notify = shelve.open("notify.db", writeback=True)
    #if info["sender"] in notify.keys() :
    #    temp = notify[info["sender"]]
    #    for user in temp :
    #        connection.ircsend(user, "%s has just said something in %s" % (info["sender"], info["channel"]))
    #        notify[iny ofo["sender"]].remove(user)
    #        notify.sync()
    #    if notify[info["sender"]] == [] :
    #        del notify[info["sender"]]
    #        notify.sync()
    #notify.close()

def happiness_detect(info) :
    """Checks to see if a smiley is in the message"""
    for emotion in [":)", ":D", "C:", "=D", "=)", "C=", "(=", "(:" "xD", ":p", ";p", "=p", ":(", "D:", "=(", "D=", "):", ")=", "=C", ":C", ":P"] :
        if emotion in info["message"] : return True
    return False
