import hashlib
arguments = ["self", "info", "args"]
helpstring = "chpass <password>"
minlevel = 2

def main(connection, info, args) :
    """Changes the sender's password"""
    salt = self.gensalt()
    connection.users["users"][info["sender"]]["password"] = hashlib.sha512(args[1]+salt).hexdigest()
    connection.users.sync()
    connection.users["users"][info["sender"]]["salt"] = salt
    connection.users.sync()
    connection.msg(info["sender"], _("You have changed your password to '%(newpass)s'") % dict(newpass=args[1]))
