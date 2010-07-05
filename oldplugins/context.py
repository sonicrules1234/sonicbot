import shelve
arguments = ["self", "info", "args"]
helpstring = "context"
minlevel = 1
def main(connection, info, args) :
    """Returns the last 10 lines in the channel"""
    context = shelve.open("context.db")
    if context.has_key(info["channel"]) :
        connection.notice(info["sender"], "\n".join(context[info["channel"]]))
    context.close()
