import urllib, json, urllib2
API_VERSION = "3.0"
class Api(object) :
    def __init__(self, login, apikey) :
        self.login = login
        self.apikey = apikey
        self.baseurl = "http://api.bit.ly/v3/"

    def shorten(self, url, justurl=True) :
        word = "shorten"
        if not url.startswith("http") :
            url = "http://" + url
        start = {"uri":url, "format":"json", "login":self.login, "apiKey":self.apikey}
        encoded = urllib.urlencode(start)
        urlobj = urllib2.urlopen(self.baseurl + word, encoded)
        data = urlobj.read()
        urlobj.close()
        pydict = json.loads(data)
        if justurl :
            return pydict[u"data"][u"url"].encode("utf8")
        else :
            return pydict

    def expand(self, urlhash, justurl=True) :
        word = "expand"
        if urlhash.startswith("http://bit.ly/") :
            usingurl = True
        elif urlhash.startswith("bit.ly") :
            usingurl = True
            urlhash = "http://" + urlhash
        else : usingurl = False
        start = {"format":"json", "login":self.login, "apiKey":self.apikey}
        if usingurl :
            start["shortUrl"] = urlhash
        else :
            start["hash"] = urlhash
        encoded = urllib.urlencode(start)
        urlobj = urllib2.urlopen(self.baseurl + word, encoded)
        data = urlobj.read()
        urlobj.close()
        pydict = json.loads(data)
        if justurl :
            return pydict[u"data"][u"expand"][0][u"long_url"].encode("utf8")
        else :
            return pydict

    def clicks(self, urlhash, justclicks=True) :
        word = "clicks"
        if urlhash.startswith("http://bit.ly/") :
            usingurl = True
        elif urlhash.startswith("bit.ly") :
            usingurl = True
            urlhash = "http://" + urlhash
        else : usingurl = False
        start = {"format":"json", "login":self.login, "apiKey":self.apikey}
        if usingurl :
            start["shortUrl"] = urlhash
        else :
            start["hash"] = urlhash
        encoded = urllib.urlencode(start)
        urlobj = urllib2.urlopen(self.baseurl + word + "?" + encoded)
        data = urlobj.read()
        urlobj.close()
        pydict = json.loads(data)
        if justclicks :
            return pydict[u"data"][u"clicks"][0][u"user_clicks"]
        else :
            return pydict

    def validate(self, x_login, x_apikey, justvalidate=True) :
        word = "validate"
        urldict = {"format":"json", "x_login":x_login, "x_apiKey":x_apikey, "login":self.login, "apiKey":self.apikey}
        encoded = urllib.urlencode(urldict)
        urlobj = urllib2.urlopen(self.baseurl + word, encoded)
        data = urlobj.read()
        pydict = json.loads(data)
        if justvalidate :
            if pydict[u"data"][u"valid"] :
                return True
            else :
                return False
        else :
            return pydict
