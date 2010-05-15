import glob
helpstring = "pluginlist"
arguments = ["self", "info", "args"]
minlevel = 1
pluginlist = []
eventlist = []
for plugin in glob.glob("plugins/*.py") :
    if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" and not plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "").startswith("on_"):
        pluginlist.append(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""))
for plugin in glob.glob("plugins/*.py") :
    if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" and plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "").startswith("on_"):
        eventlist.append(plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", ""))
pluginlist.sort()

def main(connection, info, args) :
    """Lists available plugins"""
    connection.ircsend(info["channel"], _("The available plugins are %(listofplugins)s") % dict(listofplugins=", ".join([x for x in pluginlist if x in connection.users["channels"][info["channel"]]["enabled"]])))
