import feedparser
arguments = ["self", "info", "args"]
helpstring = "lastupdate <feed url>"
minlevel = 1

def main(connection, info, args) :
    """Returns the title of the most recent item in a feed"""
    feed = feedparser.parse(args[1])
    connection.ircsend(info["channel"], "%s: '%s'" % (info["sender"], feed["items"][0]["title"].encode("utf-8")))
