import imp
pyipinfodb = imp.load_source("pyipinfodb", "pyipinfodb/pyipinfodb.py")
arguments = ["self", "info", "args"]
helpstring = "geoip <IP or hostname>"
minlevel = 1

def main(connection, info, args) :
    if args[1] != "" : connection.msg(info["channel"], "%s: %s" % (info["sender"], repr(pyipinfodb.GetCity(args[1]))))
    else : connection.msg(info["channel"], "You need to specify a host.")
