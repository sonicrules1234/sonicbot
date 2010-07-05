import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vstart <topic id>"
minlevel = 3

def main(connection, info, args, world) :
    """Starts a vote"""
    votes = shelve.open("votes.db", writeback=True)
    if not votes["networks"][connection.networkname][int(args[1]) - 1]["started"] :
        votes["networks"][connection.networkname][int(args[1]) - 1]["started"] = True
        votes.sync()
        connection.msg(info["channel"], _("The vote has started!  The topic is: '%(topic)s'.  The choices are as follows:") % dict(topic=votes["networks"][connection.networkname][int(args[1]) - 1]["topic"]))
        connection.msg(info["channel"], "\n".join(["%s %s: %s" % (_("Choice"), str(x + 1), votes["networks"][connection.networkname][int(args[1]) - 1]["choices"][x]["choice"]) for x in range(len(votes["networks"][connection.networkname][int(args[1]) - 1]["choices"]))]))
    else : connection.msg(info["channel"], _("That vote has already started!"))
    votes.close()
