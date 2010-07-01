from __future__ import division
import shelve
arguments = ["self", "info", "args"]
helpstring = "mood <nick>"
minlevel = 1

def main(connection, info, args) :
    """Returns the mood of the specified user"""
    emotions = shelve.open("emotions.db")
    person = args[1].lower()
    if person in emotions.keys() :
        rating = int(100 * (emotions[person]["happy"] / (emotions[person]["happy"] + emotions[person]["sad"])))
        emotions.close()
        if rating_compare(rating, 0, 20) : mood = _("extremely sad")
        elif rating_compare(rating, 21, 40) : mood = _("sad")
        elif rating_compare(rating, 41, 60) : mood = _("fairly neutral")
        elif rating_compare(rating, 61, 80) : mood = _("happy")
        elif rating_compare(rating, 81, 100) : mood = _("extremely happy")
        connection.ircsend(info["channel"], _("%(nick)s is %(mood1)s, with a happiness rating of %(happinessnum)s out of 100.") % dict(nick=args[1], mood1=mood, happinessnum=str(rating)))
    else :
        connection.ircsend(info["channel"], _("I have not seen %(nick)s show any emotion. :(") % dict(nick=args[1]))

def rating_compare(rating, minimum, maximum) :
    if rating >= minimum and rating <= maximum + 1 : return True
    else : return False
