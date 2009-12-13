import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vote <topic #> <choice #>"
minlevel = 1

def main(connection, info, args, world) :
    votes = shelve.open("votes.db", writeback=True)
    if votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["started"] :
        if info["sender"] not in votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["voters"] :
            votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"][int(args[2]) - 1]["votes"].append(info["sender"])
            votes.sync()
            votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["voters"].append(info["sender"])
            votes.sync()
            connection.ircsend(info["sender"], "You have successfully voted '%s' on '%s'." % (votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"][int(args[2]) - 1]["choice"], votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["topic"]))
        else : connection.ircsend(info["channel"], "%s: You have already voted!" % (info["sender"]))
    else : connection.ircsend(info["channel"], "That vote has not yet started!")
    votes.close()
