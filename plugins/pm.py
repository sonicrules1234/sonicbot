def startup(addPLuginHook, addHook, world) :
    addPluginHook(world, "pm", main, 5, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    self.pm(args[1], " ".join(args[2:]))
