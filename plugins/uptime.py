import time
def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "uptime", main, 1, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """uptime
Tells how long the bot has been running"""
    now = time.time()
    then = world.uptime
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
    passed = {("weeks"):weeks, ("days"):days, ("hours"):hours, ("minutes"):mins, ("seconds"):secs}
    self.msg(info["channel"], ("I have been running for %(length)s.") % dict(length=gettimestring(passed)))

def gettimestring(passed) :
    """Generates the appropriate string from the generated length of time"""
    timestring = ""
    for unit in [("weeks"), ("days"), ("hours"), ("minutes"), ("seconds")] :
        if unit != ("seconds") and passed[unit] != 0 :
            timestring += "%s %s, " % (passed[unit], unit)
        elif unit == ("seconds") :
            if timestring == "" : timestring = ("%(numberofseconds)s seconds") % dict(numberofseconds=passed[unit])
            else : timestring += ("and %(numberofseconds)s seconds") % dict(numberofseconds=passed[unit])
    return timestring

def makeint(number) :
    """Rounds the number"""
    rounded = int(round(number))
    if rounded > number :
        returnval = rounded - 1
    else :
        returnval = rounded
    return returnval
