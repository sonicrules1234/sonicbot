import imp
pyipinfodb = imp.load_source("pyipinfodb", "pyipinfodb/pyipinfodb.py")
arguments = ["self", "info", "args"]
helpstring = "geoip <IP or hostname>"
minlevel = 1

def main(connection, info, args) :
    connection.ircsend(info["channel"], "%s: %s" % (info["sender"], repr(pyipinfodb.GetCity(args[1]))))
