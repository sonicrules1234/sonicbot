arguments = ["self", "info", "args"]
helpstring = "admin"
minlevel = 1

def main(connection, info, args) :
    """Displays the admins from the config"""
    connection.msg(info["channel"], _("%(sender)s: The current %(botnick)s admin are: %(listofadmins)s") % dict(sender=info["sender"], botnick=self.nick, listofadmins=", ".join(self.admin)))
