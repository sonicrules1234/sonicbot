def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "detailedhelp", main, 1, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """detailedhelp <plugin>
The detailedhelp command shows more detailed help than the syntax or help command."""
    if world.plugins.has_key(args[1].lower()) :
        self.notice(info["sender"], world.plugins[args[1].lower()][0]["detailedhelp"])
