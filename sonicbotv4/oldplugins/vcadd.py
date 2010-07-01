import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vcadd <topic id> <choice>"
minlevel = 3

def main(connection, info, args, world) :
    """Adds a choice to a vote"""
    votes = shelve.open("votes.db", writeback=True)
    if not votes["networks"][connection.networkname][int(args[1]) - 1]["started"] :
        votes["networks"][connection.networkname][int(args[1]) - 1]["choices"].append({"choice":" ".join(args[2:]), "votes":[]})
        votes.sync()
        connection.msg(info["channel"], _("%(nick)s has just added the choice '%(choice)s' to the topic '%(topic)s' which has an topic id of %(topicid)s.") % dict(nick=info["sender"], choice=" ".join(args[2:]), topic=votes["networks"][connection.networkname][int(args[1]) - 1]["topic"], topicid=args[1]))
    else : connection.msg(info["channel"], _("That vote has already started!"))
    votes.close()
