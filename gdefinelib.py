import urllib, json, re
def gdefine(word) :
    data = urllib.urlencode({"callback":"a", "sl":"en", "tl":"en", "q":word})
    urlobj = urllib.urlopen("http://www.google.com/dictionary/json?" + data)
    response = urlobj.read()
    urlobj.close()
    response = response[2:].strip()
    response = response.rsplit(",", 2)
    response = "".join(response[:-2])
    #print type(response)
    responsefilter = re.sub(r"\\x3c(.+?)\\x3e", "", response)
    responsefilter = re.sub(r"\\x3c/(.+?)\\x3e", "", responsefilter)
    pydict = json.loads(responsefilter.replace("\n", "").replace("\r", "").replace("\\x27", "'"))
    #pydict = json.loads(response.replace("\n", "").replace("\r", "").replace("\\x3cem\\x3e", "").replace("\\x3c/em\\x3e", "").replace("\\x3cb\\x3e", "").replace("\\x27", "'").replace("\\x3c/b\\x3e", ""))
    #pprint.pprint(pydict, indent=4)
    entries = pydict[u'primaries'][0][u'entries']
    meaning = ""
    #partofspeech
    for entry in entries :
        if entry[u'type'] == u'meaning' :
            meaning = str(entry[u'terms'][0][u'text'])
            break
    #print meaning
    partofspeech = str(pydict[u'primaries'][0][u'terms'][0][u'labels'][0][u'text'])
    #print partofspeech
    return (partofspeech, meaning)
