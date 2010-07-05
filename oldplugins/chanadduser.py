arguments = ["self", "info", "args"]
helpstring = "chanadduser <nick>"
minlevel = 3

def main(connection, info, args) :
    """Adds a user to the channel sonicbot access list"""
    if args[1] in connection.users["users"] :
        if connection.users["users"][args[1]]["userlevel"] >= 2 :
            if connection.users["users"][args[1]]["userlevel"] == 2 :
                connection.users["users"][args[1]]["userlevel"] = 3
                connection.users.sync()
            if not connection.users["users"][args[1]].has_key("channels") :
                connection.users["users"][args[1]]["channels"] = []
                connection.users.sync()
            if info["channel"] not in connection.users["users"][args[1]]["channels"] :
                connection.users["users"][args[1]]["channels"].append(info["channel"])
                connection.users.sync()
                connection.ircsend(info["channel"], _("Added %(nick)s to the %(channel)s sonicbot access list.") % dict(nick=args[1], channel=info["channel"]))
            else :
                connection.ircsend(info["channel"], _("That user is already on this channel's sonicbot access list"))
        else : connection.ircsend(info["channel"], _("That user is not yet registered!"))
    else : connection.ircsend(info["channel"], _("That user is not yet registered!"))
