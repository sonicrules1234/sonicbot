import time, shelve
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "points [nick] [+/-number] or points [+/-]list or points -flush"
maxperday = 2
def main(connection, info, args) :
    """Gives/lists/takes points"""
    points = shelve.open("points.db", writeback=True)
    if not points.has_key("users") :
        points["users"] = {}
        points.sync()
        points["userlist"] = []
        points.sync()
    if not points.has_key("ignored") :
        points["ignored"] = {"nicks":[], "hostnames":[]}
        points.sync()
    if info["sender"].lower() not in points["users"].keys() :
        points["users"][info["sender"].lower()] = {"points":0, "outward":{}}
        points.sync()
        if len(args) == 3 :
            points["users"][info["sender"].lower()]["outward"][args[1].lower()] = 0
            points.sync() 
    if len(args) > 1 :

        if not args[1].startswith("-") and not args[1].startswith("+") :
            if args[1].lower() not in points["users"].keys() :
                points["users"][args[1].lower()] = {"points":0, "outward":{}}
                points.sync()
            if len(args) == 3 :
                if args[1].lower() not in points["users"][info["sender"].lower()]["outward"] :
                    points["users"][info["sender"].lower()]["outward"][args[1].lower()] = 0
                if args[1].lower() != info["sender"].lower() and points["users"][info["sender"].lower()]["outward"][args[1].lower()] < time.time() and verify(info["sender"].lower(), points) and info["sender"].lower() not in points["ignored"]["nicks"] and info["hostname"] not in points["ignored"]["hostnames"]:
                    sendpoints = int(args[2])
                    if sendpoints != 0 :
                        if sendpoints < -2 :
                            sendpoints = -2
                        elif sendpoints > 2 :
                            sendpoints = 2
                        points["users"][args[1].lower()]["points"] += sendpoints
                        points.sync()
                        givetake = ["given", "to"]
                        if sendpoints < 0 :
                            points["users"][info["sender"].lower()]["points"] -= 5
                            points.sync()
                            givetake = [_("taken"), _("from")]
                            connection.msg(info["channel"], _("%(sender)s: You have lost 5 points in the proccess of taking points from others") % dict(sender=info["sender"]))
                        points["users"][info["sender"].lower()]["outward"][args[1].lower()] = time.time() + (60*60*24)
                        points.sync()
                        connection.msg(info["channel"], _("%(sender)s: You have %(giveortake)s %(numberofpoints)s point(s) %(fromx)s %(nick)s") % dict(sender=info["sender"], giveortake=givetake[0], numberofpoints=str(abs(sendpoints)), fromx=givetake[1], nick=args[1]))
                        if args[1].lower() not in points["userlist"] : points["userlist"].append(args[1].lower())
                    else :
                        connection.msg(info["channel"], _("%(sender)s: %(nick)s has %(numberofpoints)s point(s).") % dict(sender=info["sender"], nick=args[1], numberofpoints=str(points["users"][args[1].lower()]["points"])))

                else : connection.msg(info["channel"], _("%(sender)s: Sorry, but you can't give/take point(s) away from that person (at this time).") % dict(sender=info["sender"]))
            if len(args) == 2 :
                connection.msg(info["channel"], _("%(sender)s: %(nick)s has %(numberofpoints)s point(s).") % dict(sender=info["sender"], nick=args[1], numberofpoints=str(points["users"][args[1].lower()]["points"])))
        else :
            if args[1] == "-reset" :
                points["user"][info["sender"].lower()]["points"] = 0
                points.sync()
                connection.msg(info["channel"], _("%(sender)s: Your points have been reset to 0") % dict(sender=info["sender"]))
            elif args[1].endswith("list") :
                pointslist = [points["users"][x]["points"] for x in points["userlist"]]
                pointslist.sort()
                userlist = points["userlist"]
                if args[1].startswith("+") : 
                    pointslist.reverse()
                    userlist.reverse()
                pointslist = pointslist[:int(args[2])]
                finalistlist = userlist
                winnerlist = []
                for point in pointslist :
                    winner = [x for x in finalistlist if points["users"][x]["points"] == point and x not in winnerlist][0]
                    winnerlist.append(winner)
                connection.msg(info["channel"], "\n".join([_("%(winnernumber)s %(nick)s with %(numberofpoints)s point(s)") % dict(winnernumber=str(winnerlist.index(winner) + 1), nick=winner, numberofpoints=points["users"][winner]["points"]) for winner in winnerlist]))
            elif args[1].endswith("compare") :
                if args[2].lower() not in points["users"].keys() :
                    points["users"][args[2].lower()] = {"points":0, "outward":{}}
                    points.sync()
                if args[3].lower() not in points["users"].keys() :
                    points["users"][args[3].lower()] = {"points":0, "outward":{}}
                    points.sync()
                connection.msg(info["channel"], _("%(nick1)s has %(numberofpoints1)s point(s) while %(nick2)s has %(numberofpoints2)s point(s).  This means %(means)s") % dict(nick1=args[2].lower(), numberofpoints1=str(points["users"][args[2].lower()]["points"]), nick2=args[3].lower(), numberofpoints2=str(points["users"][args[3].lower()]["points"]), means=compare(points, args[2].lower(), args[3].lower())))
            elif args[1].endswith("ignore") and connection.auth(info, 4) :
                if args[1].startswith("+") :
                    if args[2].lower() not in points["ignored"]["nicks"] :
                        points["ignored"]["nicks"].append(args[2].lower())
                        points.sync()
                    if args[2] in connection.hostnames.keys() :
                        if connection.hostnames[args[2]] not in points["ignored"]["hostnames"] :
                            points["ignored"]["hostnames"].append(connection.hostnames[args[2]])
                            points.sync()
                    connection.msg(info["channel"], _("%(nick)s will now be ignored") % dict(nick=args[2]))
                elif args[1].startswith("-") :
                    if args[2].lower() in points["ignored"]["nicks"] :
                        points["ignored"]["nicks"].remove(args[2].lower())
                        points.sync()
                    if args[2] in connection.hostnames.keys() :
                        if connection.hostnames[args[2]] in points["ignored"]["hostnames"] :
                            points["ignored"]["hostnames"].remove(connection.hostnames[args[2]])
                            points.sync()
                    connection.msg(info["channel"], _("%(nick)s will no longer be ignored") % dict(nick=args[2]))

    else :
        connection.msg(info["channel"], _("%(sender)s: You have %(numberofpoints)s point(s).") % dict(sender=info["sender"], numberofpoints=str(points["users"][info["sender"].lower()]["points"])))
    points.close()

def verify(sender, points) :
    history = [points["users"][sender]["outward"][x] for x in points["users"][sender]["outward"].keys()]
    history.sort()
    if len(history) in [0, 1] :
        return True
    elif time.time() >  history[-2] : return True
    else : return False

def compare(points, user1, user2) :
    if points["users"][user1]["points"] == points["users"][user2]["points"] :
        return "it is a tie"
    elif points["users"][user1]["points"] > points["users"][user2]["points"] :
        return _("%(nick1)s has %(numberofpoints)s more point(s) over %(nick2)s") % dict(nick1=user1, numberofpoints=str(points["users"][user1]["points"] - points["users"][user2]["points"]), nick2=user2)
    elif points["users"][user1]["points"] < points["users"][user2]["points"] :
        return _("%(nick1)s has %(numberofpoints)s more point(s) over %(nick2)s") % dict(nick1=user2, numberofpoints=str(points["users"][user2]["points"] - points["users"][user1]["points"]), nick2=user1)
    
