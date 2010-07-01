def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "syntax", main, 1, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """syntax <plugin>
The syntax command shows the syntax for any command, including itself."""
    if world.plugins.has_key(args[1].lower()) :
        self.msg(info["channel"], world.plugins[args[1].lower()][0]["syntax"])
