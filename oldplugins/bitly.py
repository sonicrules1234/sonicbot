import sonicbitly
arguments = ["self", "info", "args"]
helpstring = "bitly <shorten|expand|clicks> <url>"
minlevel = 2
api = sonicbitly.Api(login="sonicrules1234", apikey="R_919d42a0ee9fd225e339d73c7d54d0f9")
def main(connection, info, args) :
    if args[1] == "shorten" :
        connection.msg(info["channel"], "%(sender)s: %(url)s" % dict(sender=info["sender"], url=api.shorten(args[2])))
    elif args[1] == "expand" :
        connection.msg(info["channel"], "%(sender)s: %(url)s" % dict(sender=info["sender"], url=api.expand(args[2])))
    elif args[1] == "clicks" :
        connection.msg(info["channel"], "%(sender)s: %(clicks)d" % dict(sender=info["sender"], clicks=api.clicks(args[2])))
