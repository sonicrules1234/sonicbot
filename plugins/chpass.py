import hashlib
arguments = ["self", "info", "args"]
helpstring = "chpass <password>"
minlevel = 2

def main(connection, info, args) :
    connection.users["users"][info["sender"]]["password"] = hashlib.sha512(args[1]).hexdigest()
    connection.users.sync()
    connection.ircsend(info["sender"], "You have changed your password to '%s'" % (args[1]))
