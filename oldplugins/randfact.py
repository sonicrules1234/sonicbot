import re, urllib2
arguments = ["self", "info", "args"]
helpstring = "randfact"
minlevel = 1

def main(connection, info, args) :
    """Returns a random fact"""
    source = urllib2.urlopen("http://randomfunfacts.com/").read()
    fact = re.search(r"<strong><i>(.*)</i></strong>", source)
    connection.msg(info["channel"], "%s: %s" % (info["sender"], fact.group(1)))
