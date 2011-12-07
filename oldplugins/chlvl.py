import fnmatch
arguments = ["self", "info", "args"]
helpstring = "chlvl <nick> <level>"
minlevel = 5

def main(connection, info, args) :
    """Changes the level of a user"""
    if args[1] in connection.users["users"].keys() :
        connection.users["users"][args[1]]["userlevel"] = int(args[2])
        connection.users.sync()
        if len(args) == 4 :
            if int(args[2]) == 0 :
                self.ignorelist.append(args[3])
                connection.msg(info["channel"], len(fnmatch.filter(connection.channellist[info["channel"]], args[3])) + " users ignored with this mask")
            elif connection.users["users"][args[1]]["userlevel"] == 0 and int(args[2]) != 0:
                self.ignorelist.remove(args[3])
    else : connection.msg(info["channel"], _("No such user in my database."))
