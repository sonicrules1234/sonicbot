import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vstart <topic id>"
minlevel = 3

def main(connection, info, args, world) :
    votes = shelve.open("votes.db", writeback=True)
    if not votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["started"] :
        votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["started"] = True
        votes.sync()
        connection.ircsend(info["channel"], "The vote has started!  The topic is: '%s'.  The choices are as follows:" % (votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["topic"]))
        connection.ircsend(info["channel"], "\n".join(["Choice %s: %s" % (str(x + 1), votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"][x]["choice"]) for x in range(len(votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"]))]))
    else : connection.ircsend(info["channel"], "That vote has already started!")
    votes.close()
