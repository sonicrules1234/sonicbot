import re, urllib, urllib2
arguments = ["self", "info", "args"]
helpstring = "wra <math stuff>"
minlevel = 1

def main(connection, info, args) :
    encoded = urllib.urlencode({"i":" ".join(args[1:])})
    request = urllib2.Request("http://www.wolframalpha.com/input/", encoded)
    request.add_header('User-Agent', 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.2.15 Version/10.00')
    
    html = urllib2.urlopen(request)
    html2 = html.read()
    html.close()
    html = html2
    x = re.findall('<hr class="top" /><h2>(.*)</h2>.*<div class="output".*alt="(.*)" title=".*"\s*/>', html)
    send = []
    for y in x :
        if ">" in y[0] or ">" in y[0] or ">" in y[1] or "<" in y[1] or "\\n" in y[0] or "\\n" in y[1] :
            pass
        else :
            send.append("%s %s" % (y[0], y[1]))
    if send != [] :
        connection.msg(info["channel"], "\n".join(send))
    else : connection.msg(info["channel"], _("No (parseable) results found."))
