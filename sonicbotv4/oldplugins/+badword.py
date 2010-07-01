import shelve
arguments = ["self", "info", "args"]
helpstring = "+badword <word>"
minlevel = 3

def main(connection, info, args) :
    """Adds a word to the bad word list"""
    badwords = shelve.open("badwords.db", writeback=True)
    if not badwords.has_key(connection.host) :
        badwords[connection.host] = {}
        badwords.sync()
    if not badwords[connection.host].has_key(info["channel"]) :
        badwords[connection.host][info["channel"]] = {"users":{}, "badwords":[]}
        badwords.sync()
    if args[1] not in badwords[connection.host][info["channel"]]["badwords"] :
        badwords[connection.host][info["channel"]]["badwords"].append(args[1])
        badwords.sync()
        connection.msg(info["channel"], _("Bad word added successfully."))
    else : connection.msg(info["channel"], _("That word is already on the list"))
    badwords.close()
