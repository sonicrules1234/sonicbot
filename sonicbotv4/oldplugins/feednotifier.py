import feedparser, shelve, time
arguments = ["self", "info", "args", "world", "thread"]
helpstring = "feednotifier <title> <feed url> <on/off>"
minlevel = 3

def main(connection, info, args, world, thread) :
    """Starts the loop for checking feeds"""
    feedurl = args[-2]
    onoff = args[-1]
    title = " ".join(args[1:-2])
    if onoff == "on" :
        feeds = shelve.open("feeds-%s.db" % (world.networkname[connection.host]), writeback=True)
        feeds[feedurl] = {}
        feeds.sync()
        feeds[feedurl]["updated"] = 0
        feeds.sync()
        feeds.close()
        if not world.feeds.has_key(connection.host) :
            world.feeds[connection.host] = {}
        if not world.feeds[connection.host].has_key(info["channel"]) :
            world.feeds[connection.host][info["channel"]] = {}
        if not world.feeds[connection.host][info["channel"]].has_key(feedurl) :
            world.feeds[connection.host][info["channel"]][feedurl] = []
        if len(world.feeds[connection.host][info["channel"]][feedurl]) == 0 :
            world.feeds[connection.host][info["channel"]][feedurl].append(True)
            indexnum = len(world.feeds[connection.host][info["channel"]][feedurl]) - 1
            thread.start_new_thread(get_feed, (connection, info, args, feedurl, world, indexnum, title))
        elif not world.feeds[connection.host][info["channel"]][feedurl][-1] :
            world.feeds[connection.host][info["channel"]][feedurl].append(True)
            indexnum = len(world.feeds[connection.host][info["channel"]][feedurl]) - 1
            thread.start_new_thread(get_feed, (connection, info, args, feedurl, world, indexnum, title))
        else : connection.msg(info["channel"], _("That feed is already being tracked."))
    elif onoff == "off" :
        if feedurl in world.feeds[connection.host][info["channel"]].keys() :
                world.feeds[connection.host][info["channel"]][feedurl][-1] = False
                connection.msg(info["channel"], _("Stopped tracking feed at %(urlfeed)s") % dict(urlfeed=feedurl))
        else : connection.msg(info["channel"], _("No such feed being tracked."))

def get_feed(connection, info, args, feedurl, world, indexnum, title) :
    """Checks the feed"""
    while world.feeds[connection.host][info["channel"]][feedurl][indexnum] :
        feed = feedparser.parse(feedurl)
        feeds = shelve.open("feeds-%s.db" % (world.networkname[connection.host]), writeback=True)

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
        time.sleep(120)
