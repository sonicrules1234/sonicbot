import hashlib
arguments = ["self", "info", "args"]
helpstring = "addhost <password>"
minlevel = 1

def main(connection, info, args) :
    if info["sender"] in connection.users["users"].keys() :
        if hashlib.sha512(args[1]).hexdigest() == connection.users["users"][info["sender"]]["password"] and connection.nicks[info["sender"]] not in connection.users["users"][info["sender"]]["hostname"] :
            connection.users["users"][info["sender"]]["hostname"].append(connection.nicks[info["sender"]])
            connection.users.sync()
            connection.ircsend(info["sender"], "You have added the host '%s' to your account" % (connection.nicks[info["sender"]]))
        else : connection.ircsend(info["sender"], "Sorry, that password is incorrect or that hostname is already on your hostname list.")
    else :
        connection.ircsend(info["sender"], "You do not have an account!")
