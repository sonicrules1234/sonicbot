import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vote <topic #> <choice #>"
minlevel = 1

def main(connection, info, args, world) :
    """Lets user vote"""
    votes = shelve.open("votes.db", writeback=True)
    if votes["networks"][connection.networkname][int(args[1]) - 1]["started"] :
        if info["sender"] not in votes["networks"][connection.networkname][int(args[1]) - 1]["voters"] and ((int(args[1]) - 1) >= 1) :
            votes["networks"][connection.networkname][int(args[1]) - 1]["choices"][int(args[2]) - 1]["votes"].append(info["sender"])
            votes.sync()
            votes["networks"][connection.networkname][int(args[1]) - 1]["voters"].append(info["sender"])
            votes.sync()
            connection.msg(info["sender"], _("You have successfully voted '%(vote)s' on '%(topic)s'.") % dict(vote=votes["networks"][connection.networkname][int(args[1]) - 1]["choices"][int(args[2]) - 1]["choice"], topic=votes["networks"][connection.networkname][int(args[1]) - 1]["topic"]))
        elif (int(args[1]) -1) < 1 :
            connection.msg(info["channel"], "Invalid vote!", True)
        else : connection.msg(info["channel"], _("%(sender)s: You have already voted!") % dict(sender=info["sender"]))
    else : connection.msg(info["channel"], _("That vote has not yet started!"))
    votes.close()
