import urllib, re
import feedparser, shelve, time
arguments = ["self", "info", "args", "world", "thread"]
helpstring = "ebaytracker <title> <feed url> <on/off>"
minlevel = 3

def main(connection, info, args, world, thread) :
    """Starts the loop of checking the page for a change in price"""
    feedurl = args[-2]
    onoff = args[-1]
    title = " ".join(args[1:-2])
    if feedurl.startswith("http://cgi.ebay.com/") :
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
                thread.start_new_thread(getfeed, (connection, info, args, feedurl, world, indexnum, title))
            elif not world.feeds[connection.host][info["channel"]][feedurl][-1] :
                world.feeds[connection.host][info["channel"]][feedurl].append(True)
                indexnum = len(world.feeds[connection.host][info["channel"]][feedurl]) - 1
                thread.start_new_thread(getfeed, (connection, info, args, feedurl, world, indexnum, title))
            else : connection.msg(info["channel"], "That item is already being tracked.")
        elif onoff == "off" :
            if feedurl in world.feeds[connection.host][info["channel"]].keys() :
                    world.feeds[connection.host][info["channel"]][feedurl][-1] = False
                    connection.msg(info["channel"], ("Stopped tracking item at %(url)s") % dict(url=feedurl))
            else : connection.msg(info["channel"], ("No such item being tracked."))
    else : connection.msg(info["channel"], "That is not a valid ebay url")
def getfeed(connection, info, args, feedurl, world, indexnum, title) :
    """Checks for a change in the price on the page"""
    while world.feeds[connection.host][info["channel"]][feedurl][indexnum] :
        feeds = shelve.open("feeds-%s.db" % (world.hostnicks[connection.host]), writeback=True)
        good = urllib.urlopen(feedurl).read()
        price = re.search(r'\<td class\=\"vi\-is1\-solid vi\-is1\-tbll\"\>\<span\>\<span.*class\=\"vi\-is1\-prcp\".*\>(.*)\<\/span\>\<\/span\>\<\/td\>\<td colspan\=\"2\" class\=\"vi\-is1\-solid vi\-is1\-tblb\"\>', good).group(1)

        print "Checking feed"
        print "Recorded = %s ; Feed = %s" % (feeds[feedurl]["updated"], price)
        if price != feeds[feedurl]["updated"] and feeds[feedurl]["updated"] != 0 :
            feeds[feedurl]["updated"] = price
            feeds.sync()
            connection.msg(info["channel"], ("Another bid on %(itemtitle)s has been made!  The price is now %(newprice)s") % dict(itemtitle=title, newprice=price))
        elif feeds[feedurl]["updated"] == 0 :
            feeds[feedurl]["updated"] = price
            feeds.sync()
            connection.msg(info["channel"], ("Started tracking '%(itemtitle)s' with price of %(newprice)s.") % dict(itemtitle=title, newprice=price))
        feeds.close()
        time.sleep(120)
