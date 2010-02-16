import shelve
arguments = ["self", "info", "args", "conf", "world"]
helpstring = "rsetstatus <id> <status>"
minlevel = 4

def main(connection, info, args, conf, world) :
    """Sets a status on a report"""
    reports = shelve.open("reports-%s.db" % (world.hostnicks[connection.host]), writeback=True)
    reports["reports"][int(args[1])]["status"] = " ".join(args[2:])
    reports.sync()
    connection.ircsend(info["channel"], "Ticket #%s's status has been changed to '%s'." % (args[1], " ".join(args[2:])))
    reports.close()
