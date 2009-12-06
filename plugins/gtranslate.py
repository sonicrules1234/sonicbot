import translate
arguments = ["self", "info", "args"]
helpstring = "gtranslate <from> <to> <phrase>"
minlevel = 1

def main(connection, info, args) :
    connection.ircsend(info["channel"], '%s: "%s"' % (info["sender"], translate.translate(args[1], args[2], " ".join(args[3:])).encode("utf-8")))
    
