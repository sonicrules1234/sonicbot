def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "chnick", main, 4, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """chnick <new nick>
Changes sonicbot's nick"""
    self.rawsend("NICK %s\r\n" % (args[1]))
