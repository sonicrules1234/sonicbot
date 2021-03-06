import shelve, time
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "mail <command> [nick] [number/message]  Use 'mail help' for more details"

def main(connection, info, args) :
    """Sends, checks, or lists mail"""
    mail = shelve.open("mail.db", writeback=True)
    if args[1] == "send" :
        send_mail(connection, mail, info, ["mail"] + args[2:])
    else :
        messages = []

        if mail.has_key(info["sender"].replace("[", "").replace("]", "")) :
            if info["hostname"] in mail[info["sender"].replace("[", "").replace("]", "")]["hostname"] :
                for person in mail[info["sender"].replace("[", "").replace("]", "")]["userorder"] :
                    if mail[info["sender"].replace("[", "").replace("]", "")]["messages"][person] != {} :
                        for messaget in mail[info["sender"].replace("[", "").replace("]", "")]["messages"][person]["msgorder"] :
                            messages.append([person, messaget[0], mail[info["sender"].replace("[", "").replace("]", "")]["messages"][person][messaget[0]], messaget[1]])
                    else :
                        del mail[info["sender"].replace("[", "").replace("]", "")]["messages"][person]
                        mail[info["sender"].replace("[", "").replace("]", "")]["userorder"].remove(person)
                mail.sync()
                if len(args) == 2 :
                    if args[1] == "list" :
                        new = 0
                        for message in messages :
                            if message[3] :
                                new += 1
                        connection.msg(info["sender"], _("You have messages from %(senders)s.  %(newnum)s of these are new, and %(oldnum)s of them are old.") % dict(senders=", ".join(mail[info["sender"].replace("[", "").replace("]", "")]["userorder"]), newnum=str(new), oldnum=str(len(messages) - new)))
                    if args[1] == "help" : connection.msg(info["channel"], _("There are several subcommands for the mail command.  They are send, list, read, and delete.  list can be used like 'mail list' or 'mail list <nick>'.\nThe read and delete subcommands both need a nick and number. 'mail read <nick> <number>' and 'mail delete <nick> <number>'.\nThe available nicks and numbers can be found by using the list subcommand as forementioned.\nThe send subcommand can be used like 'mail send <nick> <message>'."))
                elif len(args) == 3 :
                    if args[1] == "list" :
                        new = 0
                        for message in mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"] :
                            if message[1] :
                                new += 1
                        connection.msg(info["sender"], _("You have %(nummessages)s messages from %(nick)s, and %(newnum)s of them are new.") % dict(nummessages=str(len(mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"])), nick=args[2], newnum=str(new)))
                elif len(args) == 4 :
                    if args[1] == "read" :
                        connection.msg(info["sender"], "[%s] <%s> %s" % (time.strftime("%x %X EEST", time.gmtime(int(mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"][int(args[3]) - 1][0]))), args[2], mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]][mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"][int(args[3]) - 1][0]]))
                        mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"][int(args[3]) - 1][1] = False
                    elif args[1] == "delete" :
                        del mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]][mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"][int(args[3]) - 1][0]]
                        mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"].pop(int(args[3]) - 1)
                        mail.sync()
                        if mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"] == [] :
                            del mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"]
                            mail.sync()
                        if mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]] == {} :
                            del mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]
                            mail[info["sender"].replace("[", "").replace("]", "")]["userorder"].remove(args[2])
                            mail.sync()
                        connection.msg(info["sender"], _("Message deleted"))
            else : connection.msg(info["sender"], _("You are not identified correctly!"))
        else : connection.msg(info["sender"], _("You are not registered!"))
    mail.sync()
    mail.close()

def send_mail(connection, mail, info, args):
    if not mail.has_key(args[1].replace("[", "").replace("]", "")) :
        connection.msg(info["channel"], _("Sorry, no such user %(nick)s in my database.") % dict(nick=args[1]))
    else :
        if not mail[args[1]]["messages"].has_key(info["sender"].replace("[", "").replace("]", "")) :
            mail[args[1].replace("[", "").replace("]", "")]["messages"][info["sender"].replace("[", "").replace("]", "")] = {}
            mail[args[1].replace("[", "").replace("]", "")]["userorder"].append(info["sender"].replace("[", "").replace("]", ""))
            mail.sync()
            mail[args[1].replace("[", "").replace("]", "")]["messages"][info["sender"].replace("[", "").replace("]", "")]["msgorder"] = []
            mail.sync()
        if len(mail[args[1].replace("[", "").replace("]", "")]["messages"][info["sender"].replace("[", "").replace("]", "")]["msgorder"]) < 10 :
            timet = str(int(time.time()))
            nogo = False 
            for message in mail[args[1]]["messages"][info["sender"].replace("[", "").replace("]", "")]["msgorder"] :
                if message[0] == timet :
                    nogo =  True
                    break
            if not nogo :
                mail[args[1].replace("[", "").replace("]", "")]["messages"][info["sender"].replace("[", "").replace("]", "")][timet] = " ".join(args[2:])
                mail.sync()
                mail[args[1].replace("[", "").replace("]", "")]["messages"][info["sender"].replace("[", "").replace("]", "")]["msgorder"].append([timet, True])
                mail.sync()
                connection.msg(info["channel"], _("%(sender)s: Your message was successfully sent.") % dict(sender=info["sender"].replace("[", "").replace("]", "")))
                mail[args[1].replace("[", "").replace("]", "")]["notify"] = True
                mail.sync()
        else : connection.msg(info["channel"], _("%(sender)s: You may only send 10 messages at a time.  You may send more once %(nick)s has checked some of your others.") % dict(sender=info["sender"].replace("[", "").replace("]", ""), nick=args[1].replace("[", "").replace("]", "")))

