import imp, socket
pyipinfodb = imp.load_source("pyipinfodb", "pyipinfodb/pyipinfodb.py")
arguments = ["self", "info", "args", "world"]
helpstring = "geoip <IP or hostname>"
minlevel = 1

def main(connection, info, args, world) :
    IPInfo = pyipinfodb.IPInfo(str(world.globalsettings[u"IPInfoDB-apikey"]))
    if args[1] != "" : connection.msg(info["channel"], "%s: %s" % (info["sender"], repr(IPInfo.GetCity([cur[4][0] for cur in socket.getaddrinfo(args[1],None) if cur[0]==2][0]))))
    else : connection.msg(info["channel"], "You need to specify a host.")
