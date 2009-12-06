arguments = ["self", "info", "args"]
helpstring = "chanreg"
minlevel = 2

def main(connection, info, args) :
    if auth(connection, info) :        
        if connection.users["users"][info["sender"]]["userlevel"] == 2 :
            connection.users["users"][info["sender"]]["userlevel"] = 3
            connection.users.sync()
        if not connection.users["users"][info["sender"]].has_key("channels") :
            connection.users["users"][info["sender"]]["channels"] = []
            connection.users.sync()
            if info["channel"] not in connection.users["users"][info["sender"]]["channels"] :
                connection.users["users"][info["sender"]]["channels"].append(info["channel"])
                connection.users.sync()
                connection.users["channels"][info["channel"]]["registered"] = True
                connection.users.sync()
                connection.ircsend(info["channel"], "%s: You have just registered %s" % (info["sender"], info["channel"]))
            else : connection.ircsend(info["channel"], "%s: You are already on this channel's sonicbot access list!" % (info["sender"]))
    else : connection.ircsend(info["channel"], "%s: You do not have at least half-ops on this channel.  If this is an error, please kick me and invite me again." % (info["sender"]))

def auth(connection, info) :
    for mode in connection.chanmodes[info["channel"]][info["sender"]] :
        if mode in ["!", "~", "@", "%"] :
            return True
    return False
