import re, urllib2
arguments = ["self", "info", "args"]
helpstring = "randfact"
needop = False

def main(connection, info, args) :
    source = urllib2.urlopen("http://randomfunfacts.com/").read()
    fact = re.search(r"<strong><i>(.*)</i></strong>", source)
    connection.ircsend(info["channel"], "%s: %s" % (info["sender"], fact.group(1)))
