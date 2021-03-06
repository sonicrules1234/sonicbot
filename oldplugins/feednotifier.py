import feedparser, shelve, time
arguments = ["self", "info", "args", "world"]
helpstring = "feednotifier <title> <feed url> <on/off>"
minlevel = 3

def main(connection, info, args, world) :
    """Starts the loop for checking feeds"""
    feedurl = args[-2]
    onoff = args[-1]
    title = " ".join(args[1:-2])
    if onoff == "on" :
        feeds = shelve.open("feeds-%s.db" % (connection.networkname), writeback=True)
        feeds[feedurl] = {}
        feeds.sync()
        feeds[feedurl]["updated"] = 0
        feeds.sync()
        feeds.close()
        if not world.feeds.has_key(connection.networkname) :
            world.feeds[connection.networkname] = {}
        if not world.feeds[connection.networkname].has_key(info["channel"]) :
            world.feeds[connection.networkname][info["channel"]] = {}
        if not world.feeds[connection.networkname][info["channel"]].has_key(feedurl) :
            world.feeds[connection.networkname][info["channel"]][feedurl] = []
        if len(world.feeds[connection.networkname][info["channel"]][feedurl]) == 0 :
            world.feeds[connection.networkname][info["channel"]][feedurl].append(True)
            indexnum = len(world.feeds[connection.networkname][info["channel"]][feedurl]) - 1
            get_feed(connection, info, args, feedurl, world, indexnum, title)
        elif not world.feeds[connection.networkname][info["channel"]][feedurl][-1] :
            world.feeds[connection.networkname][info["channel"]][feedurl].append(True)
            indexnum = len(world.feeds[connection.networkname][info["channel"]][feedurl]) - 1
            get_feed(connection, info, args, feedurl, world, indexnum, title)
        else : connection.msg(info["channel"], _("That feed is already being tracked."))
    elif onoff == "off" :
        if feedurl in world.feeds[connection.networkname][info["channel"]].keys() :
                world.feeds[connection.networkname][info["channel"]][feedurl][-1] = False
                connection.msg(info["channel"], _("Stopped tracking feed at %(urlfeed)s") % dict(urlfeed=feedurl))
        else : connection.msg(info["channel"], _("No such feed being tracked."))

def get_feed(connection, info, args, feedurl, world, indexnum, title) :
    """Checks the feed"""
    if world.feeds[connection.networkname][info["channel"]][feedurl][indexnum] :
        feed = feedparser.parse(feedurl)
        feeds = shelve.open("feeds-%s.db" % (connection.networkname), writeback=True)

        print "Checking feed"
        print "Recorded = %s ; Feed = %s" % (feeds[feedurl]["updated"], feed["items"][0]["date"])
        if feed["items"][0]["date"] != feeds[feedurl]["updated"] and feeds[feedurl]["updated"] != 0 :
            feeds[feedurl]["updated"] = feed["items"][0]["date"]
            feeds.sync()
            connection.msg(info["channel"], _("%(titleoffeed)s has changed! '%(newtitle)s'") % dict(titleoffeed=title, newtitle=feed["items"][0]["title"].encode("utf-8")))
        elif feeds[feedurl]["updated"] == 0 :
            feeds[feedurl]["updated"] = feed["items"][0]["date"]
            feeds.sync()
            connection.msg(info["channel"], _("Started tracking feed with title '%(title)s'.") % dict(title=feed["items"][0]["title"].encode("utf-8")))
        feeds.close()
        determineTiming(connection, info, args, feedurl, world, indexnum, title, get_feed)
def determineTiming(self, info, args, feedurl, world, indexnum, title, function) :
    arguments = (self, info, args, feedurl, world, indexnum, title)
    world.timer.append([world.time + 60, {"function":function, "arguments":arguments}])
