import hashlib
arguments = ["self", "info", "args"]
helpstring = "nickreg <password>"
minlevel = 1

def main(connection, info, args) :
    """Registers the sender with sonicbot"""
    if connection.users["users"][info["sender"]]["userlevel"] == 1 :
        salt = connection.gensalt()
        connection.users["users"][info["sender"]] = {"salt":salt,"password":hashlib.sha512(args[1]+salt).hexdigest(), "hostname":[connection.hostnames[info["sender"]]], "userlevel":2}
        connection.users.sync()
        connection.msg(info["sender"], _("You have registered the nick '%(nick)s' with password '%(password)s' and hostname '%(hostname)s'.  Congratulations!  You now have a user level of 2!") % dict(nick=info["sender"], password=args[1], hostname=connection.hostnames[info["sender"]]))
    else : connection.msg(info["sender"], _("Sorry, but you have already registered."))
