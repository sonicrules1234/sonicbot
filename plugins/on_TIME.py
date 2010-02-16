import time
helpstring = "This is an event plugin"
def main(connection, info, conf) :
    """Responds to CTCP TIME"""
    connection.rawsend("NOTICE %s :TIME %s\n" % (info["sender"], time.strftime("%b %d %Y, %H:%M:%S %Z")))
