arguments = ["self", "info", "args", "world"]
helpstring = "netlist"
minlevel = 1

def main(connection, info, args, world) :
    """Returns a list of networks sonicbot is on"""
    connection.msg(info["channel"], repr(world.connections.keys()))
