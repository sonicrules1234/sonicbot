import shelve, time, random, string, hashlib
arguments = ["self", "info", "args", "conf"]
minlevel = 4
helpstring = "mailman <command> <message/nick>"

def main(connection, info, args, conf) :
    """Manages sonicmail"""
    mail = shelve.open("mail.db", writeback=True)
    if args[1] == "delete" :
        if mail.has_key(args[2].replace("[", "").replace("]", "")) :
            del mail[args[2].replace("[", "").replace("]", "")]
            mail.sync()
            connection.ircsend(info["channel"], "User successfully deleted")
        else : connection.ircsend(info["channel"], "No such user")
    elif args[1] == "global" :
        timet = str(int(time.time()))
        for user in mail.keys() :
            if not mail[user]["messages"].has_key(info["sender"].replace("[", "").replace("]", "")) :
                mail[user]["messages"][info["sender"].replace("[", "").replace("]", "")] = {}
                mail[user]["userorder"].append(info["sender"].replace("[", "").replace("]", ""))
                mail.sync()
                mail[user]["messages"][info["sender"].replace("[", "").replace("]", "")]["msgorder"] = []
                mail.sync()
            mail[user]["messages"][info["sender"].replace("[", "").replace("]", "")][timet] = " ".join(args[2:])
            mail[user]["messages"][info["sender"].replace("[", "").replace("]", "")]["msgorder"].append([timet, True])
            mail[user]["notify"] = True
            mail.sync()
        mail.sync()
        connection.ircsend(info["channel"], "%s: Your global message has been sent." % (info["sender"].replace("[", "").replace("]", "")))
    elif args[1] == "passreset" :
        newpass = ""
        for x in range(6) :
            newpass += random.choice(string.letters)
        connection.ircsend(args[2], "Your password has been reset to '%s'.  Please visit %s and login using that password.  Once in, you can change it to whatever you want." % (newpass, conf.mail_url))
        mail[args[2].replace("[", "").replace("]", "")]["password"] = hashlib.sha512(newpass).hexdigest()
        mail.sync()
        connection.ircsend(info["channel"], "Password reset successfully.")
    elif args[1] == "newhost" :
        mail[args[2].replace("[", "").replace("]", "")]["hostname"].append(args[3])
        mail.sync()
        connection.ircsend(info["channel"], "Hostname changed successfully")
    elif args[1] == "autohost" :
        mail[args[2]]["hostname"].append(connection.nicks[args[2]])
        mail.sync()
        connection.ircsend(info["channel"], "%s's hostname automatically assigned to %s" % (args[2], connection.nicks[args[2]]))
    mail.close()
