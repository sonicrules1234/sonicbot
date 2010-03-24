import shelve, random
arguments = ["self", "info", "args", "world"]
minlevel = 2
helpstring = "coin <bet>"

def main(connection, info, args, world) :
    """Decides heads or tails based on the coinchance variable.   Adds or removes appropriate amount of money"""
    money = shelve.open("money-%s.db" % (world.hostnicks[connection.host]), writeback=True)
    if money.has_key(info["sender"]) :
        bet = int(args[1])
        if bet <= money[info["sender"]]["money"] and not "-" not in bet :
            answer = random.choice(money[info["sender"]]["coinchance"])
            if answer :
                money[info["sender"]]["money"] += bet
                money.sync()
                connection.ircsend(info["channel"], "Congrats %s!  You just won %s dollars!" % (info["sender"], args[1]))
            else :
                money[info["sender"]]["money"] -= bet
                money.sync()
                connection.ircsend(info["channel"], "Sorry %s!  You just lost %s dollars!" % (info["sender"], args[1]))
            if money[info["sender"]]["money"] > money[info["sender"]]["maxmoney"] :
                money[info["sender"]]["maxmoney"] = money[info["sender"]]["money"]
                money.sync()
        else : connection.ircsend(info["channel"], "%s: You don't have enough money to do that!" % (info["sender"]))
    else : connection.ircsend(info["channel"], "%s: You have not set up a money account.  If you aren't already, please register with me.  Then, say moneyreset.  After that you should be able to use this command." % (info["sender"]))
    
