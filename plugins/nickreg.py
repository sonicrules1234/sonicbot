import hashlib
arguments = ["self", "info", "args"]
helpstring = "nickreg <password>"
minlevel = 1

def main(connection, info, args) :
    if connection.users["users"][info["sender"]]["userlevel"] == 1 :
        connection.users["users"][info["sender"]] = {"password":hashlib.sha512(args[1]).hexdigest(), "hostname":[connection.nicks[info["sender"]]], "userlevel":2}
        connection.users.sync()
        connection.ircsend(info["sender"], "You have registered the nick '%s' with password '%s' and hostname '%s'.  Congratulations!  You now have a user level of 2!" % (info["sender"], args[1], connection.nicks[info["sender"]]))
    else : connection.ircsend(info["sender"], "Sorry, but you have already registered.")
