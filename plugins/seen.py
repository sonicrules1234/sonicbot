from __future__ import division
import shelve, time
arguments = ["self", "info", "args"]
helpstring = "seen <nick>"
minlevel = 1

def main(connection, info, args) :
    seendb = shelve.open("seen.db", writeback=True)
    if seendb["users"].has_key(args[1].lower()) :
        now = time.time()
        then = seendb["users"][args[1].lower()][0]
        secspassed = now - then
        weekspassed = secspassed / (60 * 60 * 24 * 7)
        weeks = int(str(weekspassed).split(".")[0])
        dayspassed = (weekspassed - weeks) * 7
        days = int(str(dayspassed).split(".")[0])
        hourspassed = (dayspassed - days) * 24
        hours = int(str(hourspassed).split(".")[0])
        minspassed = (hourspassed - hours) * 60
        mins = int(str(minspassed).split(".")[0])
        secspassed = (minspassed - mins) * 60
        secs = int(round(secspassed))
        passed = {"weeks":weeks, "days":days, "hours":hours, "minutes":mins, "seconds":secs}
        connection.ircsend(info["channel"], "The last thing %s said was: '%s'.  That was on %s, which was %s ago." % (args[1].lower(), seendb["users"][args[1].lower()][1], time.strftime("%b %d %Y, %H:%M:%S %Z", time.gmtime(then)), gettimestring(passed)))
    else : connection.ircsend(info["channel"], "I have never seen %s before." % (args[1]))

def gettimestring(passed) :
    timestring = ""
    for unit in ["weeks", "days", "hours", "minutes", "seconds"] :
        if unit != "seconds" and passed[unit] != 0 :
            timestring += "%s %s, " % (passed[unit], unit)
        elif unit == "seconds" :
            if timestring == "" : timestring = "%s seconds" % (passed[unit])
            else : timestring += "and %s seconds" % (passed[unit])
    return timestring
