arguments = ["self", "info", "args"]
helpstring = "whois <nick>"
minlevel = 1

def main(connection, info, args) :
    """Checks the user level of the specified nick"""
    if args[1] in connection.users["users"].keys() :
        connection.msg(info["channel"], _("%(nick)s has a user level of %(userlevel)s") % dict(nick=args[1], userlevel=connection.users["users"][args[1]]["userlevel"]))
        if connection.users["users"][args[1]].has_key("channels") :
            connection.msg(info["channel"], _("%(nick)s is also on these channel's access lists: %(channels)s") % dict(nick=args[1], channels=", ".join(connection.users["users"][args[1]]["channels"])))
