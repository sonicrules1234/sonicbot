import shelve, random, string, time
arguments = ["self", "info", "args", "world", "conf"]
helpstring = "report <nick> <channel> <priority of low, medium, or high> <reason>"
minlevel = 1

def main(connection, info, args, world, conf) :
    reports = shelve.open("reports-%s.db" % (world.hostnicks[connection.host]), writeback=True)
    if not reports.has_key("reports") :
        reports["reports"] = []
        reports.sync()
    reports.append({"priority":args[3], "time":time.time(), "reporter":[info["sender"].lower(), connection.nicks[info["sender"]]], "channel":args[2], "accused":args[1].lower(), "reason":" ".join(args[4:]), "password":"".join([random.choice(string.ascii_lowercase+string.ascii_uppercase) for x in range(6)]), "id":len(reports["reports"]), "status":"reported", "assigned":[], "response":{}})
    reports.sync()
    connection.ircsend(conf.staffchannel[connection.host], "%s has reported %s in %s with the reason '%s' and a priority level of %s.  This report's ID is %s." % (reports["reports"][-1]["reporter"], reports["reports"][-1]["accused"], reports["reports"][-1]["channel"], reports["reports"][-1]["reason"], reports["reports"][-1]["priority"], reports["reports"][-1]["id"]))
    reports.close()
