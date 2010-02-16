import twitter

arguments = ["self", "info", "args", "conf"]
helpstring = "tweet <message>"
minlevel = 2

def main(connection, info, args, conf) :
    """Tweets to twitter"""
    api = twitter.Api(username=conf.twituser, password=conf.twitpass)
    api.PostUpdate("[%s] %s" % (info["sender"], " ".join(args[1:])))
    connection.ircsend(info["channel"], 'http://twitter.com/%s tweeted: "[%s] %s"' % (conf.twituser, info["sender"], " ".join(args[1:])))
    
