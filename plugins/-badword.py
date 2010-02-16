import shelve
arguments = ["self", "info", "args"]
helpstring = "-badword <word>"
minlevel = 3

def main(connection, info, args) :
    """Removes a word from the bad word list"""
    badwords = shelve.open("badwords.db", writeback=True)
    if not badwords.has_key(connection.host) :
        badwords[connection.host] = {}
        badwords.sync()
    if not badwords[connection.host].has_key(info["channel"]) :
        badwords[connection.host][info["channel"]] = {"users":{}, "badwords":[]}
        badwords.sync()
    if args[1] in badwords[connection.host][info["channel"]]["badwords"] :
        badwords[connection.host][info["channel"]]["badwords"].remove(args[1])
        badwords.sync()
        connection.ircsend(info["channel"], "Bad word deleted successfully.")
    else : connection.ircsend(info["channel"], "That word is not on the list")
    badwords.close()
