arguments = ["self", "info", "args", "conf", "world"]
helpstring = "rnicks <host>"
minlevel = 1

def main(connection, info, args, conf, world) :
    connection.ircsend(info["channel"], repr(world.connections[args[1]].channels[info["channel"]]))
