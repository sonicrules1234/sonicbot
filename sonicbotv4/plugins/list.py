def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "list", main, 1, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """list
The list command lists all plugins"""
    self.msg(info["channel"], " ".join(world.plugins.keys()))
