import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "rcheck <id>"
minlevel = 4

def main(connection, info, args, world) :
    """Checks on a report"""
    reports = shelve.open("reports-%s.db" % (self.networkname), writeback=True)
    connection.msg(info["channel"], _("%(reporter)s reported %(accused)s in %(channel)s with the reason '%(reason)s' and a priority level of %(priority)s on %(timeanddate)s") % dict(reporter=reports["reports"][int(args[1])]["reporter"][0], accused=reports["reports"][int(args[1])]["accused"], channel=reports["reports"][int(args[1])]["channel"], reason=reports["reports"][int(args[1])]["reason"], priority=reports["reports"][int(args[1])]["priority"], timeanddate=time.strftime("%b %d %Y, %H:%M:%S %Z", time.gmtime(reports["reports"][int(args[1])]["time"]))))
    reports.close()
