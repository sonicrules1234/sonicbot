import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vend <topic #>"
minlevel = 3

def main(connection, info, args, world) :
    votes = shelve.open("votes.db", writeback=True)
    if votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["started"] :
        connection.ircsend(info["channel"], "The vote on '%s' has ended.  Here are the stats:" % (votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["topic"]))
        connection.ircsend(info["channel"], "\n".join(["Choice %s: '%s' got %s votes" % (str(x + 1), votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"][x]["choice"], str(len(votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"][x]["votes"]))) for x in range(len(votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"]))]))
        scores = [len(votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"][x]["votes"]) for x in range(len(votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"]))]
        winningscore = max(scores)
        winners = [x["choice"] for x in votes["networks"][world.hostnicks[connection.host]][int(args[1]) - 1]["choices"] if len(x["votes"]) == winningscore]
        if len(winners) == 1 : connection.ircsend(info["channel"], "The winner is %s!" % (winners[0]))
        else : connection.ircsend(info["channels"], "The winners with a tie in 1st place are: %s and %s." % (", ".join(winners[:-1]), winners[-1]))
        votes["networks"][world.hostnicks[connection.host]].pop(int(args[1]) - 1)
        votes.sync()
    else : connection.ircsend(info["channel"], "That vote has not yet started!")
    votes.close()
