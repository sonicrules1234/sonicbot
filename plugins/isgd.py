import urllib
arguments = ["self", "info", "args"]
helpstring = "isgd <url>"
minlevel = 1

def main(connection, info, args) :
    if args[1].startswith("http://is.gd/") :
        newurl = urllib.urlopen(args[1]).geturl()
    else : newurl = urllib.urlopen("http://is.gd/api.php?longurl=" + args[1]).read()
    connection.ircsend(info["channel"], "%s: %s" % (info["sender"], newurl))
