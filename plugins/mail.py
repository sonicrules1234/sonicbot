import shelve, time
arguments = ["self", "info", "args"]
helpstring = "mail <nick> <message>"
minlevel = 1

def main(connection, info, args) :
    mail = shelve.open("mail.db", writeback=True)
    if not mail.has_key(args[1].replace("[", "").replace("]", "")) :
        connection.ircsend(info["channel"], "Sorry, no such user %s in my database." % (args[1]))
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
                connection.ircsend(info["channel"], "%s: Your message was successfully sent." % (info["sender"].replace("[", "").replace("]", "")))
                mail[args[1].replace("[", "").replace("]", "")]["notify"] = True
                mail.sync()
        else : connection.ircsend(info["channel"], "%s: You may only send 10 messages at a time.  You may send more once %s has checked some of your others." % (info["sender"].replace("[", "").replace("]", ""), args[1].replace("[", "").replace("]", "")))
    mail.close()
