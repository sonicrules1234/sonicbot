
import shelve
def main(connection, info, conf) :
    if info["sender"] in conf.admin.keys() :
        if info["hostname"] in conf.admin[info["sender"]] :
            for mode in conf.modeonjoin[connection.host] :
                connection.rawsend("MODE %s +%s %s\n" % (info["channel"], mode, info["sender"]))
    if info["sender"] != conf.nick and info["channel"] in conf.avchans : connection.rawsend("MODE %s +v %s\n" % (info["channel"], info["sender"]))
    mail = shelve.open("mail.db", writeback=True)
    if info["sender"].replace("[", "").replace("]", "") in mail.keys() :
        newsenders = []
        for person in mail[info["sender"].replace("[", "").replace("]", "")]["userorder"] :
            for messaget in mail[info["sender"].replace("[", "").replace("]", "")]["messages"][person]["msgorder"] :
               if person not in newsenders and messaget[1] : newsenders.append(person)
        if len(newsenders) > 0 :
            connection.ircsend(info["sender"], "You have new message(s) from %s" % (", ".join(newsenders)))
    if info["channel"] in conf.welcomechans : connection.ircsend(info["channel"], "Welcome to %s, %s" % (info["channel"], info["sender"]))
    info["sender"] = info["sender"].lower()
    notify = shelve.open("notify.db", writeback=True)
    if info["sender"] in notify.keys() :
        temp = notify[info["sender"]]
        for user in temp :
            connection.ircsend(user, "%s has just joined %s" % (info["sender"], info["channel"]))
            notify[info["sender"]].remove(user)
            notify.sync()
        if notify[info["sender"]] == [] :
            del notify[info["sender"]]
            notify.sync()
    notify.close()
