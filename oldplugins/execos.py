import commands
helpstring = "execos <command>"
arguments = ["self", "info", "args", "conf"]
minlevel = 5
def main(connection, info, args, conf) :
    """Executes a command in the terminal"""
    if info["sender"] == conf.owner : connection.msg(info["channel"], commands.getoutput(" ".join(args[1:])))
