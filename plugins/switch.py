from __future__ import division
import shelve, time
arguments = ["self", "info", "args"]
helpstring = "switch"
minlevel = 1

def main(connection, info, args) :
    now = time.time()
    then = 1264836600
    secspassed = then - now
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
    passed = {"week(s)":weeks, "day(s)":days, "hour(s)":hours, "minute(s)":mins, "second(s)":secs}
    connection.ircsend("There is %s until Freenode is supposed to switch from Hyperion to ircd-seven." % (gettimestring(passed)))
def gettimestring(passed) :
    timestring = ""
    for unit in ["week(s)", "day(s)", "hour(s)", "minute(s)", "second(s)"] :
        if unit != "second(s)" and passed[unit] != 0 :
            timestring += "%s %s, " % (passed[unit], unit)
        elif unit == "second(s)" :
            if timestring == "" : timestring = "%s second(s)" % (passed[unit])
            else : timestring += "and %s second(s)" % (passed[unit])
    return timestring

def makeint(number) :
    rounded = int(round(number))
    if rounded > number :
        returnval = rounded - 1
    else :
        returnval = rounded
    return returnval
