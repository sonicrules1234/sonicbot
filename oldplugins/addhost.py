import hashlib
arguments = ["self", "info", "args"]
helpstring = "addhost <password>"
minlevel = 1

def main(connection, info, args) :
    """Adds the senders host to his/her account"""
    if info["sender"] in connection.users["users"].keys() :
        if hashlib.sha512(args[1]+connection.users["users"][info["sender"]]["salt"]).hexdigest() == connection.users["users"][info["sender"]]["password"] and connection.hostnames[info["sender"]] not in connection.users["users"][info["sender"]]["hostname"] :
            connection.users["users"][info["sender"]]["hostname"].append(connection.hostnames[info["sender"]])
            connection.users.sync()
            connection.msg(info["sender"], _("You have added the host '%(host)s' to your account") % dict(host=connection.hostnames[info["sender"]]))
        else : connection.msg(info["sender"], _("Sorry, that password is incorrect or that hostname is already on your hostname list."))
    else :
        connection.msg(info["sender"], _("You do not have an account!"))
