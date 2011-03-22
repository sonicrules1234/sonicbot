import shelve, time
def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "delfactoid", main, 1, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """delfactoid <factoid>
Removes a factoid"""
    factoids = shelve.open("factoids.db", writeback=True)
    factoid = args[1]
    deletion = time.time()
    deleter = info["whois"]
    deleternick = info["sender"]
    deleterident = info["whois"].split("!", 1)[1].split("@")[0]
    deleterhost = info["hostname"]
    definition = "This factoid was deleted by %(deleter)s at %(deletion)d" % {"deleter":deleter, "deletion":deletion}
    if not factoids.has_key(factoid) :
        factoids[factoid] = {}
        factoids.sync()
    factoids[factoid][info["channel"]] = {"definition":definition, "deletiontime":deletion, "deleter":deleter, "deleternick":deleternick, "deleterident":deleterident, "deleterhost":deleterhost}
    factoids.sync()
    factoids.close()
    self.msg(info["channel"], "Factoid removed.", True)
