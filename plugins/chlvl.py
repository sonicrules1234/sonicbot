arguments = ["self", "info", "args"]
helpstring = "chlvl <nick> <level>"
minlevel = 5

def main(connection, info, args) :
    """Changes the level of a user"""
    if args[1] in connection.users["users"].keys() :
        connection.users["users"][args[1]]["userlevel"] = int(args[2])
        connection.users.sync()
    else : connection.ircsend(info["channel"], "No such user in my database.")
