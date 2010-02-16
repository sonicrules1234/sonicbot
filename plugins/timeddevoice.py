import thread, time
arguments = ["self", "info", "args"]
helpstring = "timeddevoice <nick> <minutes>"
minlevel = 3
def main(connection, info, args) :
    """Devoices somebody, waits, then revoices them"""
    connection.rawsend("MODE %s -v %s\r\n" % (info["channel"], args[1]))
    thread.start_new_thread(devoice, (int(args[2]) * 60, connection, info, args[1]))
def devoice(timer, connection, info, args1) :
    """Waits and then revoices"""
    time.sleep(timer)
    connection.rawsend("MODE %s +v %s\r\n" % (info["channel"], args1))
