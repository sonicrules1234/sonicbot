import glob
plugin_list = []
for plugin in glob.glob("plugins/*.py") :
    if plugin != "plugins/__init__.py" and plugin != "plugins\\__init__.py" :
        exec("import %s" % (plugin.replace("plugins\\", "").replace("plugins/", "").replace(".py", "")))
