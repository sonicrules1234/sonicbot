def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "pm", main, 5, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """pm <nick> <message>
Makes a private message"""
    self.pm(args[1], " ".join(args[2:]))
