import time
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "bday <MM/DD/YYYY>"
def main(connection, info, args) :
    """Calculates the number of days until the user's birthday"""
    birthd = args[1]
    error = 0
    error2 = 0
    try :
        bday = time.strptime(birthd, "%m/%d/%Y")
        birthday = time.strftime("%B %d %y", bday)
    except : error = 1
    if error == 1 :
        try :
            origyear = birthd[(len(birthd) - 4):]
            birthd = birthd[:(len(birthd) - 4)] + "1992"
            bday = time.strptime(birthd, "%m/%d/%Y")
            birthday = time.strftime("%B %d %y", bday)
        except : error2 = 1
    if error2 == 1 :
        send("An error occured")
    elif error2 == 0 and error == 1 :
        birthday = time.strftime("%B %d %y", bday)
        now = time.gmtime()
        if bday[1] == now[1] and bday[2] == now[2] :
            years = now[0] - int(origyear)
            days = 0
        elif bday[1] < now[1] or (bday[1] == now[1] and bday[2] < now[2]) :
            years = now[0] - int(origyear)
            nextbday = time.strptime(birthday[:(len(birthday) - 2)] + str(now[0] + 1), "%B %d %Y")
            secstillbday = int(time.mktime(nextbday)) - int(time.time())
            days = int(secstillbday / (60 * 60 * 24))
        else :
            years = now[0] - int(origyear) - 1
            nextbday = time.strptime(birthday[:(len(birthday) - 2)] + str(now[0]), "%B %d %Y")
            secstillbday = int(time.mktime(nextbday)) - int(time.time())
            days = int(secstillbday / (60 * 60 * 24))
        if days != 0 : connection.ircsend(info["channel"], "You are %s years old and have %s days until your next birthday." % (str(years), str(days)))
        else : connection.ircsend(info["channel"], "Today is your birthday.  You are %s years old" % (str(years)))
    elif error == 0 :
        bday = time.strptime(birthd, "%m/%d/%Y")
        birthday = time.strftime("%B %d %y", bday)
        now = time.gmtime()
        if bday[1] == now[1] and bday[2] == now[2] :
            years = now[0] - bday[0]
            days = 0
        elif bday[1] < now[1] or (bday[1] == now[1] and bday[2] < now[2]) :
            years = now[0] - bday[0]
            nextbday = time.strptime(birthday[:(len(birthday) - 2)] + str(now[0] + 1), "%B %d %Y")
            secstillbday = int(time.mktime(nextbday)) - int(time.time())
            days = int(secstillbday / (60 * 60 * 24))
        else :
            years = now[0] - bday[0] - 1
            nextbday = time.strptime(birthday[:(len(birthday) - 2)] + str(now[0]), "%B %d %Y")
            secstillbday = int(time.mktime(nextbday)) - int(time.time())
            days = int(secstillbday / (60 * 60 * 24))
        if days != 0 : connection.ircsend(info["channel"], "You are %s years old and have %s days until your next birthday." % (str(years), str(days)))
        else : connection.ircsend(info["channel"], "Today is your birthday.  You are %s years old." % (str(years)))
