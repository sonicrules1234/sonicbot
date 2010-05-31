import shelve, time
arguments = ["connection", "info", "args"]
minlevel = 1
helpstring = "addquote <quote>"

def main(connection, info, args) :
    qdb = shelve.open("quotes.db", writeback=True)
    if not qdb.has_key("quotes") :
        qdb["quotes"] = []
        qdb.sync()
    qdb.append("quote":" ".join(args[1:]), "time":time.time(), "method":"IRC", "info":info, "deleted":False})
    qdb.sync()
    connection.ircsend(info["channel"], "Quote %(quotenum)d added successfully." % dict(quotenum=len(qdb["quotes"])))
    qdb.close()
