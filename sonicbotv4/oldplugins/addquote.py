import shelve, time
arguments = ["self", "info", "args"]
minlevel = 1
helpstring = "addquote <quote>"

def main(connection, info, args) :
    qdb = shelve.open("quotes.db", writeback=True)
    if not qdb.has_key("quotes") :
        qdb["quotes"] = []
        qdb.sync()
    qdb["quotes"].append({"quote":" ".join(args[1:]), "time":time.time(), "method":"IRC", "info":info, "deleted":False})
    qdb.sync()
    connection.msg(info["channel"], "Quote #%(quotenum)d added successfully." % dict(quotenum=len(qdb["quotes"])))
    qdb.close()
