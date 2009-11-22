import shelve
arguments = ["self", "info", "args"]
helpstring = "context"
needop = False
def main(connection, info, args) :
    context = shelve.open("context.db")
    if context.has_key(info["channel"]) :
        connection.ircsend(info["sender"], "\n".join(context[info["channel"]]))
    context.close()
