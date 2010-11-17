import imp
pyipinfodb = imp.load_source("pyipinfodb", "pyipinfodb/pyipinfodb.py")
arguments = ["self", "info", "args", "world"]
helpstring = "geoip <IP or hostname>"
minlevel = 1

def main(connection, info, args, world) :
    IPInfo = pyipinfodb.IPInfo(world.globalsettings["IPInfoDB-apikey"])
    if args[1] != "" : connection.msg(info["channel"], "%s: %s" % (info["sender"], repr(IPInfo.GetCity(args[1]))))
    else : connection.msg(info["channel"], "You need to specify a host.")
