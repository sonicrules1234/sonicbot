arguments = ["self", "info", "args", "world"]
helpstring = "rnicks <host>"
minlevel = 1

def main(connection, info, args, world) :
    """Returns the nicks of the same channel on another network"""
    connection.msg(info["channel"], repr(world.connections[args[1]].channellist[info["channel"]]))
