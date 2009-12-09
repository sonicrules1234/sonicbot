import feedparser, shelve, thread, time
arguments = ["self", "info", "args", "conf", "world", "thread"]
helpstring = "wikinotifier <feed url>"
minlevel = 4

def main(connection, info, args, conf, world, thread) :
    feedurl = args[-2]
    onoff = args[-1]
    title = args[1:-3]
    if onoff == "on" :
        feeds = shelve.open("feeds-%s.db" % (world.hostnicks[connection.host]), writeback=True)
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
            thread.start_new_thread(get_feed, (connection, info, args, args[1], world, indexnum, title))
        elif not world.feeds[connection.host][info["channel"]][feedurl][-1] :
            world.feeds[connection.host][info["channel"]][feedurl].append(True)
            indexnum = len(world.feeds[connection.host][info["channel"]][feedurl]) - 1
            thread.start_new_thread(get_feed, (connection, info, args, args[1], world, indexnum, title))
        else : connection.ircsend(info["channel"], "That feed is already being tracked.")
    elif onoff == "off" :
        if feedurl in world.feeds[connection.host][info["channel"]].keys() :
                world.feeds[connection.host][info["channel"]][feedurl][-1] = False
                connection.ircsend(info["channel"], "Stopped tracking feed at %s" % (feedurl))
        else : connection.ircsend(info["channel"], "No such feed being tracked.")

def get_feed(connection, info, args, feedurl, world, indexnum, title) :
    while world.feeds[connection.host][info["channel"]][feedurl][indexnum] :
        feed = feedparser.parse(feedurl)
        feeds = shelve.open("feeds-%s.db" % (world.hostnicks[connection.host]), writeback=True)
        print "Checking feed"
        print "Recorded = %s ; Feed = %s" % (feeds[feedurl]["updated"], feed["items"][0]["date"])
        if feed["items"][0]["date"] != feeds[feedurl]["updated"] and feeds[feedurl]["updated"] != 0 :
            feeds[feedurl]["updated"] = feed["items"][0]["date"]
            feeds.sync()
            connection.ircsend(info["channel"], "The wiki at %s has changed! %s changed %s.  Take a look at %s for the difference." % (feedurl, feed["items"][0]["author"].encode("utf-8"), feed["items"][0]["title"].encode("utf-8"), feed["items"][0]["link"].encode("utf-8")))
        elif feeds[feedurl]["updated"] == 0 :
            feeds[feedurl]["updated"] = feed["items"][0]["date"]
            feeds.sync()
            connection.ircsend(info["channel"], "Started tracking feed with title '%s'." % (feed["items"][0]["title"].encode("utf-8")))
        feeds.close()
        time.sleep(120)
