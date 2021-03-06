import urllib, urllib2, re, htmlentitydefs
arguments = ["self", "info", "args"]
helpstring = "google <result #> <query>"
minlevel = 1
def main(connection, info, args) :
    """Googles the query"""
    if args[1].isdigit() :
        params = urllib.urlencode({'start' : args[1], 'q': " ".join(args[2:])})
        request = urllib2.Request("http://google.com/search?%s" % (params))
        request.add_header('User-Agent', 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.2.15 Version/10.00')
        f = urllib2.urlopen(request)
        source = f.read()
        resultlist = re.findall(r'<h3 class="r"><a href="(http://.+?)"', source)
        resultlist2 = re.findall(r'<span class=st>(.+?)<br>', source)
        connection.ircsend(info["channel"], "%s - %s" % (resultlist[0], partfilter(resultlist2[0].replace("<em>", "\x02").replace("</em>", "\x02").replace("<b>", "\x02").replace("</b>", "\x02"))))
def partfilter(inputtext) :
    for entity in htmlentitydefs.entitydefs.keys() :
        inputtext = inputtext.replace("&%s;" % (entity), htmlentitydefs.entitydefs[entity])
    return inputtext
