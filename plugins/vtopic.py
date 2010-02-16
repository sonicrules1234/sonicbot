import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "vtopic <topic>"
minlevel = 3

def main(connection, info, args, world) :
    """Sets the topic of a vote"""
    votes = shelve.open("votes.db", writeback=True)
    if not votes.has_key("networks") :
        votes["networks"] = {world.hostnicks[connection.host]:[]}
        votes.sync()
    if not votes["networks"].has_key(world.hostnicks[connection.host]) :
        votes["networks"][world.hostnicks[connection.host]] = []
        votes.sync()
    votes["networks"][world.hostnicks[connection.host]].append({"topic":" ".join(args[1:]), "choices":[], "started":False, "voters":[]})
    votes.sync()
    connection.ircsend(info["channel"], "The topic '%s' has been given the topic id of %s" % (" ".join(args[1:]), len(votes["networks"][world.hostnicks[connection.host]])))
    votes.close()
