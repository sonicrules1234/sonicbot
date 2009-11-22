arguments = ["self", "info", "args", "conf", "world"]
helpstring = "rnicks <host>"
needop = False

def main(connection, info, args, conf, world) :
    connection.ircsend(info["channel"], repr(world.connections[args[1]].channels[info["channel"]]))
