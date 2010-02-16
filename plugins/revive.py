arguments = ["self", "info", "args", "conf"]
helpstring = "revive <multiple>"
minlevel = 3

def main(connection, info, args, conf) :
    """Voices everybody in the channel"""
    count = 0
    userlist = []
    for user in connection.channels[info["channel"]] :
        count += 1
        if count < int(args[1]) + 1 : 
            userlist.append(user)
        else :
            connection.rawsend("MODE %s +%s %s\n" % (info["channel"], "v" * count, " ".join(userlist)))
            count = 0
            userlist = []
    if count != 0 :
        connection.rawsend("MODE %s +%s %s\n" % (info["channel"], "v" * count, " ".join(userlist)))
