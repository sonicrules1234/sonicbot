import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vcadd <topic id> <choice>"
minlevel = 3

def main(connection, info, args, world) :
    """Adds a choice to a vote"""
    votes = shelve.open("votes.db", writeback=True)
    if not votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["started"] :
        votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"].append({"choice":" ".join(args[2:]), "votes":[]})
        votes.sync()
        connection.ircsend(info["channel"], "%s has just added the choice '%s' to the topic '%s' which has an topic id of %s." % (info["sender"], " ".join(args[2:]), votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["topic"], args[1]))
    else : connection.ircsend(info["channel"], "That vote has already started!")
    votes.close()
