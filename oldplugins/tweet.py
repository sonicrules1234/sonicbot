import twitter

arguments = ["self", "info", "args"]
helpstring = "tweet <message>"
minlevel = 2

def main(connection, info, args) :
    """Tweets to twitter"""
    api = twitter.Api(username=connection.twituser, password=connection.twitpass)
    api.PostUpdate("[%s] %s" % (info["sender"], " ".join(args[1:])))
    connection.msg(info["channel"], _('http://twitter.com/%(botnick)s tweeted: "[%(nick)s] %(message)s"') % dict(botnick=connection.twituser, nick=info["sender"], message=" ".join(args[1:])))
    
