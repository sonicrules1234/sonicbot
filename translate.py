##This not mine, I found it somewhere on google code

import re
import urllib


import simplejson as json
import yaml




class UrlOpener(urllib.FancyURLopener):
        version = "py-gtranslate/1.0"


class InvalidLanguage(Exception): pass


base_uri = "http://ajax.googleapis.com/ajax/services/language/translate"
default_params = {'v': '1.0'}
langs = yaml.load(file('langs.yml', 'r').read())


def translate(src, to, phrase):
        src = langs.get(src, src)
        to = langs.get(to, to)
        if not src in langs.values() or not to in langs.values():
                raise InvalidLanguage("%s=>%s is not a valid translation" % (src, to))
        
        args = default_params.copy()
        args.update({
                'langpair': '%s%%7C%s' % (src, to),
                'q': urllib.quote_plus(phrase),
        })
        argstring = '%s' % ('&'.join(['%s=%s' % (k,v) for (k,v) in args.iteritems()]))
        resp = json.load(UrlOpener().open('%s?%s' % (base_uri, argstring)))
        try:
                return resp['responseData']['translatedText']
        except:
                # should probably warn about failed translation
                return phrase
