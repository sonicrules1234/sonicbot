arguments = ["self", "info", "args"]
helpstring = "whois <nick>"
minlevel = 1

def main(connection, info, args) :
    """Checks the user level of the specified nick"""
    if args[1] in connection.users["users"].keys() :
        connection.ircsend(info["channel"], "%s has a user level of %s" % (args[1], connection.users["users"][args[1]]["userlevel"]))
        if connection.users["users"][args[1]].has_key("channels") :
            connection.ircsend(info["channel"], "%s is also on these channel's access lists: %s" % (args[1], ", ".join(connection.users["users"][args[1]]["channels"])))
