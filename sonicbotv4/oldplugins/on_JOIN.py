
import shelve
def main(connection, info) :
    """Runs every time sonicbot sees somebody join a channel"""
    if info["sender"] in connection.admin.keys() :

        if info["hostname"] in connect.admin[info["sender"]] :

            if connection.host in connection.modeonjoin.keys() :
                for mode in connection.modeonjoin[connection.host] :
                    connection.rawsend("MODE %s +%s %s\n" % (info["channel"], mode, info["sender"]))
#    if info["sender"] != self.nick and info["channel"] in self.avchans : connection.rawsend("MODE %s +v %s\n" % (info["channel"], info["sender"]))
    mail = shelve.open("mail.db", writeback=True)
    if info["sender"].replace("[", "").replace("]", "") in mail.keys() :
        newsenders = []
        for person in mail[info["sender"].replace("[", "").replace("]", "")]["userorder"] :
            for messaget in mail[info["sender"].replace("[", "").replace("]", "")]["messages"][person]["msgorder"] :
               if person not in newsenders and messaget[1] : newsenders.append(person)
        if len(newsenders) > 0 :
            connection.ircsend(info["sender"], _("You have new message(s) from %(nick(s") % dict(nick=", ".join(newsenders)))
    mail.close()
#    if info["channel"] in conf.welcomechans and info["sender"] != conf.nick : connection.ircsend(info["channel"], _("Welcome to %(channel)s, %(nick)s") % dict(channel=info["channel"], nick=info["sender"]))
    info["sender"] = info["sender"].lower()
    notify = shelve.open("notify.db", writeback=True)
    if info["sender"] in notify.keys() :
        temp = notify[info["sender"]]
        for user in temp :
            connection.ircsend(user, _("%(nick)s has just joined %(channel)s") % dict(nick=info["sender"], channel=info["channel"]))
            notify[info["sender"]].remove(user)
            notify.sync()
        if notify[info["sender"]] == [] :
            del notify[info["sender"]]
            notify.sync()
    notify.close()
    memos = shelve.open("memos.db", writeback=True)
    if memos.has_key(info["sender"].lower()) :
        for memo in memos[info["sender"].lower()] :
            connection.ircsend(info["channel"], "%(sender)s: %(memoer)s sent you a memo! '%(memo)s'" % {"sender":info["sender"], "memoer":memo["sender"], "memo":memo["message"]})
        memos[info["sender"].lower()] = []
        memos.sync()
    memos.close()
