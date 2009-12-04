arguments = ["self", "info", "args"]
needop = True
helpstring = "enable <plugin>"

def main(connection, info, args) :
    if args[1] not in connection.users["channels"][info["channel"]]["enabled"] :
        connection.users["channels"][info["channel"]]["enabled"].append(args[1])
        connection.users.sync()
        connection.ircsend(info["channel"], "The %s plugin has been enabled in this channel" % (args[1]))
    else : connection.ircsend(info["channel"], "That plugin is not disabled!")
