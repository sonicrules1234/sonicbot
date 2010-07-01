import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vend <topic #>"
minlevel = 3

def main(connection, info, args, world) :
    """Ends a vote and returns the results"""
    votes = shelve.open("votes.db", writeback=True)
    if votes["networks"][connection.networkname][int(args[1]) - 1]["started"] :
        connection.msg(info["channel"], _("The vote on '%(topic)s' has ended.  Here are the stats:") % dict(topic=votes["networks"][connection.networkname][int(args[1]) - 1]["topic"]))
        connection.msg(info["channel"], "\n".join([_("Choice %(choicenum)s: '%(choicestring)s' got %(numvotes)s votes") % dict(choicenum=str(x + 1), choicestring=votes["networks"][connection.networkname][int(args[1]) - 1]["choices"][x]["choice"], numvotes=str(len(votes["networks"][connection.networkname][int(args[1]) - 1]["choices"][x]["votes"]))) for x in range(len(votes["networks"][connection.networkname][int(args[1]) - 1]["choices"]))]))
        scores = [len(votes["networks"][connection.networkname][int(args[1]) - 1]["choices"][x]["votes"]) for x in range(len(votes["networks"][connection.networkname][int(args[1]) - 1]["choices"]))]
        winningscore = max(scores)
        winners = [x["choice"] for x in votes["networks"][connection.networkname][int(args[1]) - 1]["choices"] if len(x["votes"]) == winningscore]
        if len(winners) == 1 : connection.msg(info["channel"], "The winner is %s!" % (winners[0]))
        else : connection.msg(info["channel"], _("The winners with a tie in 1st place are: %(people)s and %(lastperson)s.") % dict(people=", ".join(winners[:-1]), lastperson=winners[-1]))
        votes["networks"][connection.networkname].pop(int(args[1]) - 1)
        votes.sync()
    else : connection.msg(info["channel"], _("That vote has not yet started!"))
    votes.close()
