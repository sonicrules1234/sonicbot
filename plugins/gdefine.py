arguments = ["self", "info", "args"]
needop = False
helpstring = "gdefine <phrase>"

def main(connection, info, args) :
    connection.ircsend(info["channel"], "%s: %s" % (info["sender"], gdefine(" ".join(args[1:]))))

def gdefine(word):
	import urllib,urllib2,re
	req=urllib2.Request("http://www.google.com/search?%s"%urllib.urlencode({'q':'define:'+word,'oe':'utf-8','ie':'utf-8'}))
	req.add_header('User-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009090216 Ubuntu/9.04 (jaunty) Firefox/3.0.14')
	return re.sub('&([^;]+);',lambda found: {'quot':'"',"amp":'&'}[found.groups()[0]],re.findall('<li>([^<]+)',urllib2.build_opener().open(req).read())[0])
