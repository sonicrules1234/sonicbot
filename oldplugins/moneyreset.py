import shelve
arguments = ["self", "info", "args", "world"]
minlevel = 2
helpstring = "moneyreset"

def main(connection, info, args, world) :
    """Resets a users money"""
    money = shelve.open("money-%s.db" % (connection.networkname), writeback=True)
    money[info["sender"]] = {"money":100000, "maxmoney":100000, "items":[], "coinchance":[True for x in range(50)] + [False for x in range(50)]}
    money.sync()
    connection.msg(info["channel"], _("%(sender)s: Your money data has been reset.") % dict(sender=info["sender"]))
    
