import thread, time
arguments = ["self", "info", "args"]
helpstring = "timedban <nick> <minutes>"
minlevel = 3
def main(connection, info, args) :
    """Starts a timed ban"""
    if args[1] in connection.nicks.keys() :
        target = "*!*@%s" % (connection.nicks[args[1]])
    else : target = "%s*!*@*" % (args[1])
    connection.rawsend("MODE %s +b %s\n" % (info["channel"], target))
    thread.start_new_thread(unban, (connection,"MODE %s -b %s\n" % (info["channel"], target), int(args[2]) * 60))
def unban(connection, msg, timer) :
    """Waits and then unbans"""
    time.sleep(timer)
    connection.rawsend(msg)
