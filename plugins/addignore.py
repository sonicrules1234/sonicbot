import shelve, time
def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "addignore", main, 4, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """addignore <hostmask>
Adds a hostmask to the bot's ignore list"""
    if args[1].lower() not in self.ignorelist :
        self.ignorelist.append(args[1].lower())
        self.msg(info["channel"], "Ignore added.")
    else :
        self.msg(info["channel"], "That hostmask is already being ignored.")
