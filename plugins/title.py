import re, urllib2
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "title <url>"

def main(connection, info, args) :
    link = urllib2.urlopen(args[1])
    title = re.search(r"\<title\>(.+?)\</title\>", link.read(2000).replace("\n", "").replace("\t", "")).group(1)
    connection.ircsend(info["channel"], '%s: "%s"' % (info["sender"], title))
