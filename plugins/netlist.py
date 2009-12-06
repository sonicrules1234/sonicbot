arguments = ["self", "info", "args", "world"]
helpstring = "netlist"
minlevel = 1

def main(connection, info, args, world) :
    connection.ircsend(info["channel"], repr(world.connections.keys()))
