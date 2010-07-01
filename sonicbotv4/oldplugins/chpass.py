import hashlib
arguments = ["self", "info", "args"]
helpstring = "chpass <password>"
minlevel = 2

def main(connection, info, args) :
    """Changes the sender's password"""
    connection.users["users"][info["sender"]]["password"] = hashlib.sha512(args[1]).hexdigest()
    connection.users.sync()
    connection.msg(info["sender"], _("You have changed your password to '%(newpass)s'") % dict(newpass=args[1]))
