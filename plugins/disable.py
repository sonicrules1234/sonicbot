arguments = ["self", "info", "args"]
needop = True
helpstring = "disable <plugin>"

def main(connection, info, args) :
    if args[1] in connection.users["channels"][info["channel"]]["enabled"] :
        connection.users["channels"][info["channel"]]["enabled"].remove(args[1])
        connection.users.sync()
        connection.ircsend(info["channel"], "The %s plugin has been disabled in this channel" % (args[1]))
    else : connection.ircsend(info["channel"], "That plugin is not enabled!")
