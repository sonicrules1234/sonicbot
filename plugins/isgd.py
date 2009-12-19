import urllib
arguments = ["self", "info", "args"]
helpstring = "isgd <url>"
minlevel = 1

def main(connection, info, args) :
    connection.ircsend(info["channel"], "%s: %s" % (info["sender"], getnewurl(args[1])))

def real2isgd(url) :
    newurl = urllib.urlopen("http://is.gd/api.php?longurl=" + url).read()
    return newurl

def isgd2real(url) :
    newurl = urllib.urlopen(url).geturl()
    return newurl

def getnewurl(oldurl) :
    if oldurl.startswith("http://is.gd/") :
        return isgd2real(oldurl)
    else : return real2isgd(oldurl)
