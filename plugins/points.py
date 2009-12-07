import time, shelve
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "points [nick] [+/-number] or points [+/-]list or points -flush"

def main(connection, info, args) :
    points = shelve.open("points.db", writeback=True)
    if not points.has_key("users") :
        points["users"] = {}
        points.sync()
        points["userlist"] = []
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
                if args[1].lower() != info["sender"].lower() and points["users"][info["sender"].lower()]["outward"][args[1].lower()] < time.time() :
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
                            givetake = ["taken", "from"]
                            connection.ircsend(info["channel"], "%s: You have lost 5 points in the proccess of taking points from others" % (info["sender"]))
                        points["users"][info["sender"].lower()]["outward"][args[1].lower()] = time.time() + (60*60*24)
                        points.sync()
                        connection.ircsend(info["channel"], "%s: You have %s %s point(s) %s %s" % (info["sender"], givetake[0], str(abs(sendpoints)), givetake[1], args[1]))
                        if args[1].lower() not in points["userlist"] : points["userlist"].append(args[1].lower())
                    else :
                        connection.ircsend(info["channel"], "%s: %s has %s point(s)." % (info["sender"], args[1], str(points["users"][args[1].lower()]["points"])))

                else : connection.ircsend(info["channel"], "%s: Sorry, but you can't give/take point(s) away from that person (at this time)." % (info["sender"]))
            if len(args) == 2 :
                connection.ircsend(info["channel"], "%s: %s has %s point(s)." % (info["sender"], args[1], str(points["users"][args[1].lower()]["points"])))
        else :
            if args[1] == "-reset" :
                points["user"][info["sender"].lower()]["points"] = 0
                points.sync()
                connection.ircsend(info["channel"], "%s: Your points have been reset to 0" % (info["sender"]))
            elif args[1].endswith("list") :
                pointslist = [points["users"][x]["points"] for x in points["userlist"]]
                pointslist.sort()
                userlist = points["userlist"]
                if args[1].startswith("+") : 
                    pointslist.reverse()
                    userlist.reverse()
                pointslist = pointslist[:5]
                finalistlist = userlist
                winnerlist = []
                for point in pointslist :
                    winner = [x for x in finalistlist if points["users"][x]["points"] == point and x not in winnerlist][0]
                    winnerlist.append(winner)
                connection.ircsend(info["channel"], "\n".join(["%s %s with %s point(s)" % (str(winnerlist.index(winner) + 1), winner, points["users"][winner]["points"]) for winner in winnerlist]))
                
    else :
        connection.ircsend(info["channel"], "%s: You have %s point(s)." % (info["sender"], str(points["users"][info["sender"].lower()]["points"])))
    points.close()
