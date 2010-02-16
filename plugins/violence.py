import random, random
arguments = ["self", "info", "args", "conf"]
minlevel = 1
helpstring = "violence <nick>"
verbs = ["slaps", "kicks", "barfs on", "punches", "force feeds", "squishes", "stomps on", "bodyslams", "shoots", "smacks", "compresses", "crunches"]
adjectives = ["sweet", "dirty", "corny", "ugly", "magical", "smelly", "gross old", "old", "tasty", "messy", "blue", "red", "yellow", "pink", "purple", "green", "classic", "stinky"]
nouns = ["man", "woman", "admin", "IRCop", "car", "fish", "bomb", "missile", "computer", "keyboard", "football", "set of speakers", "monopoly set"]
def main(connection, info, args, conf) :
    """Generates a random attack"""
    if args[1].lower() in [conf.owner.lower(), conf.nick.lower(), "himself", "herself", "itself"] :
        target = info["sender"]
        if target.lower() in [conf.owner.lower(), conf.nick.lower(), "himself", "herself", "itself"] :
            randomlist = connection.channels[info["channel"]]
            randomlist.remove(conf.owner)
            randomlist.remove(conf.nick)
            target = random.choice(randomlist)
    else : target = args[1]
    connection.ircsend(info["channel"], "\x01ACTION %s %s with a %s %s.\x01" % (random.choice(verbs), target, random.choice(adjectives), random.choice(nouns)))
