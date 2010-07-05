import shelve
arguments = ["self", "info", "args", "conf", "world"]
helpstring = "rsetstatus <id> <status>"
minlevel = 4

def main(connection, info, args, conf, world) :
    """Sets a status on a report"""
    reports = shelve.open("reports-%s.db" % (connection.networkname), writeback=True)
    reports["reports"][int(args[1])]["status"] = " ".join(args[2:])
    reports.sync()
    connection.msg(info["channel"], _("Ticket #%(ticketnumber)s's status has been changed to '%(newstatus)s'.") % dict(ticketnumber=args[1], newstatus=" ".join(args[2:])))
    reports.close()
