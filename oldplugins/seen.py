from __future__ import division
import shelve, time
arguments = ["self", "info", "args"]
helpstring = "seen <nick>"
minlevel = 1

def main(connection, info, args) :
    """Calculates the amount of time it has been since the specified nick was last seen."""
    seendb = shelve.open("seen.db", writeback=True)
    if seendb["users"].has_key(args[1].lower()) :
        now = time.time()
        then = seendb["users"][args[1].lower()][0]
        secspassed = now - then
        weekspassed = secspassed / (60 * 60 * 24 * 7)
        weeks = makeint(weekspassed)
        dayspassed = (weekspassed - weeks) * 7
        days = makeint(dayspassed)
        hourspassed = (dayspassed - days) * 24
        hours = makeint(hourspassed)
        minspassed = (hourspassed - hours) * 60
        mins = makeint(minspassed)
        secspassed = (minspassed - mins) * 60
        secs = int(round(secspassed))
        passed = {_("weeks"):weeks, _("days"):days, _("hours"):hours, _("minutes"):mins, _("seconds"):secs}
        connection.msg(info["channel"], _("The last thing %(nick)s said was: '%(message)s'.  That was on %(dateandtime)s, which was %(length)s ago.") % dict(nick=args[1].lower(), message=seendb["users"][args[1].lower()][1], dateandtime=time.strftime("%b %d %Y, %H:%M:%S %Z", time.gmtime(then)), length=gettimestring(passed)))
    else : connection.msg(info["channel"], _("I have never seen %(nick)s before.") % dict(nick=args[1]))

def gettimestring(passed) :
    """Generates the appropriate string from the generated length of time"""
    timestring = ""
    for unit in [_("weeks"), _("days"), _("hours"), _("minutes"), _("seconds")] :
        if unit != _("seconds") and passed[unit] != 0 :
            timestring += "%s %s, " % (passed[unit], unit)
        elif unit == _("seconds") :
            if timestring == "" : timestring = _("%(numberofseconds)s seconds") % dict(numberofseconds=passed[unit])
            else : timestring += _("and %(numberofseconds)s seconds") % dict(numberofseconds=passed[unit])
    return timestring

def makeint(number) :
    """Rounds the number"""
    rounded = int(round(number))
    if rounded > number :
        returnval = rounded - 1
    else :
        returnval = rounded
    return returnval
