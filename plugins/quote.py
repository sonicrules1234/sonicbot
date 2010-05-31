import shelve, time
arguments = ["connection", "info", "args"]
minlevel = 1
helpstring = "quote <quote #>"

def main(connection, info, args) :
    qdb = shelve.open("quotes.db")
    if not qdb.has_key("quotes") :
        connection.ircsend(info["channel"], "Sorry, the quote database is empty!")
    else :
        if int(args[1]) <= len(qdb["quotes"]) :
            connection.ircsend(info["channel"], "Quote #%(quotenum)s: %(quote)s" % dict(quotenum=args[1], qdb["quotes"][int(args[1]) - 1]))
        else : connection.ircsend(info["channel"], "No such quote!")
    qdb.close()
