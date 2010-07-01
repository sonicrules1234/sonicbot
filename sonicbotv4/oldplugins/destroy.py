arguments = ["self", "info", "args", "conf"]
helpstring = "destroy <multiple>"
minlevel = 3

def main(connection, info, args, conf) :
    """Devoices all non-admins in the channel"""
    count = 0
    userlist = []
    for user in connection.channels[info["channel"]] :
        if user not in conf.admin and user != conf.nick :
            
            if count < int(args[1]) + 1 : 
                userlist.append(user)
            else :
                connection.rawsend("MODE %s -%s %s\n" % (info["channel"], "v" * count, " ".join(userlist)))
                userlist = []
                count = 0
            count += 1
    if count != 0 :
        connection.rawsend("MODE %s -%s %s\n" % (info["channel"], "v" * count, " ".join(userlist)))
