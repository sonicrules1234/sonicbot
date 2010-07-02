def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "chnick", main, 1, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    self.rawsend("NICK %s\r\n" % (args[1]))
