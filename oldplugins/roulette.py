import random
arguments = ["self", "info", "args"]
helpstring = "roulette"
minlevel = 1

def main(connection, info, args) :
    """Kicks on the probablity in the prob variable"""
    prob = [2, 3]
    chances = [True for x in range(prob[0])] + [False for y in range(prob[1])]
    choice = random.choice(chances)
    if choice :
        connection.rawsend("KICK %s %s :You lost roulette!\n" % (info["channel"], info["sender"]))
    else : connection.msg(info["channel"], "*click*")
