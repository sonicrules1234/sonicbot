import fnmatch
arguments = ["self", "info", "args"]
helpstring = "chlvl <nick> <level> [hostmask]"
minlevel = 5

def main(connection, info, args) :
    """Changes the level of a user"""
    if args[1] in connection.users["users"].keys() :
        if len(args) == 4 :
            if int(args[2]) == 0 :
                if args[3] not in connection.ignorelist : connection.ignorelist.append(args[3])
                connection.msg(info["channel"], str(len(fnmatch.filter([connection.whoislist[x] for x in connection.channellist[info["channel"]]], args[3]))) + " users ignored with this mask")
            elif connection.users["users"][args[1]]["userlevel"] == 0 and int(args[2]) != 0:
                if args[3] in connection.ignorelist: connection.ignorelist.remove(args[3])
        connection.users["users"][args[1]]["userlevel"] = int(args[2])
        connection.users.sync()
    else : connection.msg(info["channel"], _("No such user in my database."))
