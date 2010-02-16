arguments = ["self", "info", "args", "conf", "world"]
helpstring = "rnicks <host>"
minlevel = 1

def main(connection, info, args, conf, world) :
    """Returns the nicks of the same channel on another network"""
    connection.ircsend(info["channel"], repr(world.connections[args[1]].channels[info["channel"]]))
