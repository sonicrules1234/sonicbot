arguments = ["self", "info", "args"]
helpstring = "chanreg"
minlevel = 2

def main(connection, info, args) :
    """Registers a channel with sonicbot"""
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
            connection.msg(info["channel"], _("%(sender)s: You have just registered %(channel)s") % dict(sender=info["sender"], channel=info["channel"]))
        else : connection.msg(info["channel"], _("%(sender)s: You are already on this channel's sonicbot access list!") % dict(sender=info["sender"]))
    else : connection.msg(info["channel"], _("%(sender)s: You do not have at least half-ops on this channel.  If this is an error, please kick me and invite me again.") % dict(sender=info["sender"]))

def auth(connection, info) :
    """Checks to see if the sender has at least half-ops in the channel"""
    for mode in connection.chanmodes[info["channel"]][info["sender"]] :
        if mode in ["!", "~", "@", "%", "&"] :
            return True
    return False
