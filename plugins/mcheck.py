import shelve, time
arguments = ["self", "info", "args"]
needop = False
helpstring = "mcheck <command> [nick] [number]"

def main(connection, info, args) :
    messages = []
    mail = shelve.open("mail.db", writeback=True)
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
                    connection.ircsend(info["sender"], "You have messages from %s.  %s of these are new, and %s of them are old." % (", ".join(mail[info["sender"].replace("[", "").replace("]", "")]["userorder"]), str(new), str(len(messages) - new)))
                if args[1] == "help" : connection.ircsend(info["channel"], "There are several subcommands for ;mcheck.  They are list, read, and delete.  list can be used like ;mcheck list or ;mcheck list <nick>.\nThe read and delete subcommands both need a nick and number. ;mcheck read <nick> <number> and ;mcheck delete <nick> <number>.\nThe available nicks and numbers can be found by using the list subcommand as forementioned.")
            elif len(args) == 3 :
                if args[1] == "list" :
                    new = 0
                    for message in mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"] :
                        if message[1] :
                            new += 1
                    connection.ircsend(info["sender"], "You have %s messages from %s, and %s of them are new." % (str(len(mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"])), args[2], str(new)))
            elif len(args) == 4 :
                if args[1] == "read" :
                    connection.ircsend(info["sender"], "[%s] <%s> %s" % (time.strftime("%x %X EEST", time.gmtime(int(mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"][int(args[3]) - 1][0]))), args[2], mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]][mail[info["sender"].replace("[", "").replace("]", "")]["messages"][args[2]]["msgorder"][int(args[3]) - 1][0]]))
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
                    connection.ircsend(info["sender"], "Message deleted")
        else : connection.ircsend(info["sender"], "You are not identified correctly!")
    else : connection.ircsend(info["sender"], "You are not registered!")
    mail.sync()
    mail.close()
