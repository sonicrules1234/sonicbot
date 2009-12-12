import shelve
arguments = ["self", "info", "args"]
helpstring = "committracker <git url> <stop/start>"
minlevel = 5

def main(connection, info, args) :
    commits = shelve.open("commits.db", writeback=True)
    if not commits.has_key("networks") :
        commits["networks"] = {}
        commits.sync()
    if not commits["networks"].has_key(connection.host) :
        commits["networks"][connection.host] = {}
        commits.sync()
    if not commits["networks"][connection.host].has_key(info["channel"]) :
        commits["networks"][connection.host][info["channel"]] = []
        commits.sync()
    if args[2] == "start" :
        if args[1] not in commits["networks"][connection.host][info["channel"]] :
            commits["networks"][connection.host][info["channel"]].append(args[1])
            commits.sync()
            connection.ircsend(info["channel"], "Now tracking %s" % (args[1]))
        else : connection.ircsend(info["channel"], "That url is already being tracked!")
    elif args[2] == "stop" :
        if args[1] in commits["networks"][connection.host][info["channel"]] :
            commits["networks"][connection.host][info["channel"]].remove(args[1])
            commits.sync()
            connection.ircsend(info["channel"], "No longer tracking %s" % (args[1]))
        else : connection.ircsend(info["channel"], "That url is not being being tracked yet!")
