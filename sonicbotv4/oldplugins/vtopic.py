import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vtopic <topic>"
minlevel = 3

def main(connection, info, args, world) :
    """Sets the topic of a vote"""
    votes = shelve.open("votes.db", writeback=True)
    if not votes.has_key("networks") :
        votes["networks"] = {connection.networkname:[]}
        votes.sync()
    if not votes["networks"].has_key(connection.networkname) :
        votes["networks"][connection.networkname] = []
        votes.sync()
    votes["networks"][connection.networkname].append({"topic":" ".join(args[1:]), "choices":[], "started":False, "voters":[]})
    votes.sync()
    connection.msg(info["channel"], _("The topic '%(topic)s' has been given the topic id of %(id)d") % dict(topic=" ".join(args[1:]), id=len(votes["networks"][connection.networkname])))
    votes.close()
