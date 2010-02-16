helpstring = "This is an event plugin"
def main(connection, info, conf) :
    """Runs every time sonicbot is invited to a channel"""
    connection.rawsend("JOIN %s\n"%info['words'][3][1:])
    connection.ircsend(conf.owner, "Joining %s after being invited..." % (info['words'][3][1:]))
