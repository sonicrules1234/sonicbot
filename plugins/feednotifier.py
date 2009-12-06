import feedparser, shelve, time
arguments = ["self", "info", "args", "conf", "world", "thread"]
helpstring = "feednotifier <feed url>"
minlevel = 3

def main(connection, info, args, conf, world, thread) :
    feedurl = args[1]
    if len(args) == 2 :
        feeds = shelve.open("feeds.db", writeback=True)
        feeds[feedurl] = {}
        feeds.sync()
        feeds[feedurl]["updated"] = 0
        feeds.sync()
        feeds.close()
        
        world.feeds[feedurl] = True
        thread.start_new_thread(get_feed, (connection, info, args, args[1], world))

    elif len(args) == 3 :
        if feedurl in world.feeds :
            if args[2] == "off" :
                world.feeds[feedurl] = False
                connection.ircsend(info["channel"], "Stopped tracking feed at %s" % (feedurl))
        else : connection.ircsend(info["channel"], "No such feed being tracked.")

def get_feed(connection, info, args, feedurl, world) :
    while world.feeds[feedurl] :
        feed = feedparser.parse(feedurl)
        feeds = shelve.open("feeds.db", writeback=True)
        print "Checking feed"
        print "Recorded = %s ; Feed = %s" % (feeds[feedurl]["updated"], feed["items"][0]["date"])
        if feed["items"][0]["date"] != feeds[feedurl]["updated"] and feeds[feedurl]["updated"] != 0 :
            feeds[feedurl]["updated"] = feed["items"][0]["date"]
            feeds.sync()
            connection.ircsend(info["channel"], "The feed at %s has changed! '%s'" % (feedurl, feed["items"][0]["title"].encode("utf-8")))
        elif feeds[feedurl]["updated"] == 0 :
            feeds[feedurl]["updated"] = feed["items"][0]["date"]
            feeds.sync()
            connection.ircsend(info["channel"], "Started tracking feed with title '%s'." % (feed["items"][0]["title"].encode("utf-8")))
        feeds.close()
        time.sleep(120)
