import shelve
arguments = ["self", "info", "args"]
minlevel = 2
helpstring = "shellvote <nick>"

def main(connection, info, args) :
    votes = shelve.open("shellvotes.db", writeback=True)
    if info["sender"].lower() in ["sonicrules1234", "shadowwolf", "[3]nertia", "juju2143", "lenswipe"] :
        if votes["users"].has_key(args[1].lower()) :
            votes["users"][args[1].lower()]["voters"].append(info["sender"])
            votes.sync()
            connection.ircsend(info["sender"], "Vote successful.")
            if len(votes["users"][args[1].lower()]["votes"]) == 3 :
                connection.ircsend(info["channel"], "%s now has the minimum number of votes to get a shell.  An admin now needs to use ;createshell %s when %s is here." % (args[1], args[1]))
        else :
            connection.ircsend(info["channel"], "That user has not used the ;initiate command yet.")
    else : connection.ircsend(info["channel"], "%s: You are not a ##5709 admin." % (info["sender"]))
    votes.close()
