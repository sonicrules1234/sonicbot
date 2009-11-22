from __future__ import division
import shelve
arguments = ["self", "info", "args"]
helpstring = "mood <nick>"
needop = False

def main(connection, info, args) :
    emotions = shelve.open("emotions.db")
    person = args[1].lower()
    if person in emotions.keys() :
        rating = int(100 * (emotions[person]["happy"] / (emotions[person]["happy"] + emotions[person]["sad"])))
        emotions.close()
        if rating_compare(rating, 0, 20) : mood = "extremely sad"
        elif rating_compare(rating, 21, 40) : mood = "sad"
        elif rating_compare(rating, 41, 60) : mood = "fairly neutral"
        elif rating_compare(rating, 61, 80) : mood = "happy"
        elif rating_compare(rating, 81, 100) : mood = "extremely happy"
        connection.ircsend(info["channel"], "%s is %s, with a happiness rating of %s out of 100." % (args[1], mood, str(rating)))
    else :
        connection.ircsend(info["channel"], "I have not seen %s show any emotion. :(" % (args[1]))

def rating_compare(rating, minimum, maximum) :
    if rating >= minimum and rating <= maximum + 1 : return True
    else : return False
