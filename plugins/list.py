def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "list", main, 1, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """list
The list command lists all plugins"""
    pluginlist = world.plugins.keys()
    pluginlist.sort()
    self.msg(info["channel"], "I will send you the list of plugins in a notice because there are too many to list here", reply=True)
    self.msg(info["sender"], " ".join(pluginlist))
