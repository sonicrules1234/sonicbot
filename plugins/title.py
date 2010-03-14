import re, urllib2
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "title <url>"

def main(connection, info, args) :
    """Gets the title of a url"""
    link = urllib2.urlopen(args[1])
    title = re.search(r"\<title\>(.+?)\</title\>", link.read(2000).replace("\n", "").replace("\t", "").replace("\r", "")).group(1) #\r being stripped is because of an UnrealIRCd bug
    connection.ircsend(info["channel"], '%s: "%s"' % (info["sender"], title))
