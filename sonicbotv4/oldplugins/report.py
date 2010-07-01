import shelve, random, string, time
arguments = ["self", "info", "args", "world"]
helpstring = "report <nick> <channel> <priority of low, medium, or high> <reason>"
minlevel = 1

def main(connection, info, args, world) :
    """Makes a report."""
    reports = shelve.open("reports-%s.db" % (connection.networkname), writeback=True)
    if not reports.has_key("reports") :
        reports["reports"] = []
        reports.sync()
    reports["reports"].append({"priority":args[3], "time":time.time(), "reporter":[info["sender"].lower(), connection.hostnames[info["sender"]]], "channel":args[2], "accused":args[1].lower(), "reason":" ".join(args[4:]), "password":"".join([random.choice(string.ascii_lowercase+string.ascii_uppercase) for x in range(6)]), "id":len(reports["reports"]), "status":"reported", "assigned":[], "response":{}})
    reports.sync()
    connection.msg(info["sender"], _("The incident has been reported"))
    connection.msg(connection.staffchannel[connection.host], _("%(sender)s has reported %(nick)s in %(channel)s with the reason '%(reason)s' and a priority level of %(level)s.  This report's ID is %(id)s.") % dict(sender=reports["reports"][-1]["reporter"][0], nick=reports["reports"][-1]["accused"], channel=reports["reports"][-1]["channel"], reason=reports["reports"][-1]["reason"], level=reports["reports"][-1]["priority"], id=reports["reports"][-1]["id"]))
    reports.close()
