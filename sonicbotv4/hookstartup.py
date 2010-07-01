import imp, glob, os, traceback

def main(self, world) :
    world.loaded = True
    for x in glob.glob("essentials/*.py") :
        plugin = imp.load_source(x.replace("essentials\\", "").replace("essentials/", "").replace(".py", ""), x)
        self.addHook(plugin.keyword, plugin, plugin.minlevel, plugin.arguments)
    hookOldPlugins(self, world)
    hookPlugins(self, world)

def hookPlugins(self, world) :
    oldplugins = {}
    for filename in glob.glob("plugins/*.pyc") :
        os.remove(filename)
    for plugin in glob.glob("plugins/*.py") :
        if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" :
            oldplugins[plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "")] = imp.load_source(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""), plugin)
    for plugin in oldplugins.keys() :
        x = oldplugins[plugin]
        x.startup(addHookPlugin, self.addHook, world)
def addHookWorld(world, keyword, function, minlevel, arguments) :
    if not world.hooks.has_key(keyword) :
        world.hooks[keyword] = []
    world.hooks[keyword].append({"minlevel":minlevel, "arguments":arguments, "function":function})


def hookOldPlugins(self, world) :
    oldplugins = {}
    for filename in glob.glob("oldplugins/*.pyc") :
        os.remove(filename)
    for xplugin in glob.glob("oldplugins/*.py") :
        if xplugin != "oldplugins/__init__.py" and xplugin != "oldplugins\\__init__.py" :
            try :
                y = xplugin.replace("oldplugins\\", "").replace("oldplugins/", "").replace(".py", "")
                if y.startswith("on_") :
                    print "Loading old", y[3:]
                    self.addHook(y[3:], imp.load_source(xplugin.replace("oldplugins\\", "").replace("oldplugins/", "").replace(".py", ""), xplugin), 1, ["self", "info"])
                else : oldplugins[xplugin.replace("oldplugins\\", "").replace("oldplugins/", "").replace(".py", "")] = imp.load_source(xplugin.replace("oldplugins\\", "").replace("oldplugins/", "").replace(".py", ""), xplugin)
            except : traceback.print_exc()
    for xplugin in oldplugins.keys() :
        x = oldplugins[xplugin]
        addHookOldPlugin(world, xplugin.lower(), x, x.minlevel, x.arguments, x.helpstring, x.main.__doc__)
def addHookOldPlugin(world, keyword, function, minlevel, arguments, helpstring, detailedhelp) :
    if not world.plugins.has_key(keyword) :
        world.plugins[keyword] = []
    world.plugins[keyword].append({"minlevel":minlevel, "arguments":arguments, "function":function.main, "syntax":helpstring, "detailedhelp":detailedhelp})
def addHookPlugin(world, keyword, function, minlevel, arguments) :
    if not world.plugins.has_key(keyword) :
        world.plugins[keyword.lower()] = []
    docs = function.__doc__
    docs = docs.replace("\r", "")
    lines = docs.split("\n")
    helpstring = lines[0]
    detailedhelp = "\n".join(lines[1:])
    world.plugins[keyword.lower()].append({"minlevel":minlevel, "arguments":arguments, "function":function, "syntax":helpstring, "detailedhelp":detailedhelp})
