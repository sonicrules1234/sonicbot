import shelve
arguments = ["self", "info", "args", "world"]
minlevel = 2
helpstring = "coin <bet>"

def main(connection, info, args, world) :
    """Decides heads or tails based on the coinchance variable.   Adds or removes appropriate amount of money"""
    money = shelve.open("money-%s.db" % (world.networkname), writeback=True)
    if money.has_key(info["sender"]) :
        bet = int(args[1])
        if bet <= money[info["sender"]]["money"] and bet >= 1 :
            answer = random.choice(money[info["sender"]]["coinchance"])
            if answer :
                money[info["sender"]]["money"] += bet
                money.sync()
                connection.msg(info["channel"], _("Congrats %(sender)s!  You just won %(num)s dollars!") % dict(sender=info["sender"], num=args[1]))
            else :
                money[info["sender"]]["money"] -= bet
                money.sync()
                connection.msg(info["channel"], _("Sorry %(sender)s!  You just lost %(num)s dollars!") % dict(sender=info["sender"], num=args[1]))
            if money[info["sender"]]["money"] > money[info["sender"]]["maxmoney"] :
                money[info["sender"]]["maxmoney"] = money[info["sender"]]["money"]
                money.sync()
        else : connection.msg(info["channel"], _("%(sender)s: You don't have enough money to do that!") % dict(sender=info["sender"]))
    else : connection.msg(info["channel"], _("%(sender)s: You have not set up a money account.  If you aren't already, please register with me.  Then, say moneyreset.  After that you should be able to use this command.") % dict(sender=info["sender"]))
    
