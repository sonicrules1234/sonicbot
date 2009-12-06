import commands
helpstring = "execos <command>"
arguments = ["self", "info", "args", "conf"]
minlevel = 5
def main(connection, info, args, conf) :
    if info["sender"] == conf.owner : connection.ircsend(info["channel"], commands.getoutput(" ".join(args[1:])))
