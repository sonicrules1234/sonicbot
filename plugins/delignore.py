import shelve, time
def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "delignore", main, 4, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """delignore <hostmask>
Removes a hostmask from the bot's ignore list"""
    if args[1].lower() in self.ignorelist :
        self.ignorelist.remove(args[1].lower())
        self.msg(info["channel"], "Ignore removed.")
    else :
        self.msg(info["channel"], "That hostmask is not on the ignore list.")
