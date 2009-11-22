arguments = ["self", "info", "args", "world"]
helpstring = "netlist"
needop = False

def main(connection, info, args, world) :
    connection.ircsend(info["channel"], repr(world.connections.keys()))
