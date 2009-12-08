import shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "rcheck <id>"
minlevel = 4

def main(connection, info, args, world) :
    reports = shelve.open("reports-%s.db" % (world.hostnicks[connection.host]), writeback=True)
    connection.ircsend(info["channel"], "%s reported %s in %s with the reason '%s' and a priority level of %s on %s" % (reports["reports"][int(args[1])]["reporter"], reports["reports"][int(args[1])]["accused"], reports["reports"][int(args[1])]["channel"], reports["reports"][int(args[1])]["reason"], reports["reports"][int(args[1])]["priority"], time.strftime("%b %d %Y, %H:%M:%S %Z", time.gmtime(reports["reports"][int(args[1])]["time"]))))
    reports.close()
