import translate
arguments = ["self", "info", "args"]
helpstring = "gtranslate <from> <to> <phrase>"
minlevel = 1

def main(connection, info, args) :
    connection.ircsend(info["channel"], '%s: "%s"' % (info["sender"], partfilter(translate.translate(args[1], args[2], " ".join(args[3:])).encode("utf-8"))))
    
def partfilter(inputtext) :
    for entity in htmlentitydefs.entitydefs.keys() :
        inputtext = inputtext.replace("&%s;" % (entity), htmlentitydefs.entitydefs[entity])
    return inputtext
