import shelve, time
def startup(addPluginHook, addHook, world) :
    addPluginHook(world, "addfactoid", main, 1, ["self", "info", "args", "world"])
def main(self, info, args, world) :
    """addfactoid <factoid> is <definition>
Adds a factoid"""
    factoids = shelve.open("factoids.db", writeback=True)
    factoid = args[1]
    definition = info["message"].split(" is ", 1)[1]
    creation = time.time()
    creator = info["whois"]
    creatornick = info["sender"]
    creatorident = info["whois"].split("!", 1)[1].split("@")[0]
    createrhost = info["hostname"]
    if not factoids.has_key(factoid) :
        factoids[factoid] = {}
        factoids.sync()
    factoids[factoid][info["channel"]] = {"definition":definition, "creationtime":creation, "creator":creator, "creatornick":creatornick, "creatorident":creatorident, "creatorhost":creatorhost}
    factoids.sync()
    factoids.close()
    self.msg("Factoid added.")
