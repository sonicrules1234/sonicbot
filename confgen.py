print "Welcome to the sonicbot config generator!"
print "I just be asking you a few questions and then you will be able to run sonicbot!"
print "First of all, what is your IRC nick?"
owner = raw_input()
print "Nice to meet you, %s!  What do you want the your sonicbot's nick to be?" % (owner)
nick = raw_input()
ident = "sonicbot"
realname = "sonicbot"
connectcommands = {}
print "When %s identifies, what password should it use?  (Just press enter to use none)" % (nick)
bpass = raw_input()
print "What trigger character should %s use?" % (nick)
prefix = raw_input()
print "Do you want to use the twitter plugin? (y/n)"
response = raw_input()
if response.lower() in ["yes", "y"] :
    print "What is the twitter username?"
    twituser = raw_input()
    print "What is the twitter password?"
    twitpass = raw_input()
else :
    twituser = ""
    twitpass = ""
print "Now we will move on to networks"

networks = {}
print "Please give this network a name."
networkname = raw_input()
print "What is the hostname of %s?" % (networkname)
hostname = raw_input()
networks[hostname] = {"hostnick":networkname}
print "What port will you use for %s?" % (hostname)
port = input()
networks[hostname]["port"] = port
print "Do you want the bot to use ssl on this network? (y/n)"
yesno = raw_input()
if yesno.lower() in ["yes", "y"] :
    ssl = True
else : ssl = False
networks[hostname]["ssl"] = ssl
print "Do you want the bot to use IPv6 on this network? (y/n)"
yesno = raw_input()
if yesno.lower() in ["yes", "y"] :
    ipv6 = True
else : ipv6 = False
networks[hostname]["ipv6"] = ipv6
print "What is your hostname or vhost on this network?"
vhosts = [raw_input()]
print "Please type all the channels you want the bot to automatically join when connecting to this network, seperating them with spaces"
channels = raw_input().split(" ")
networks[hostname]["channels"] = channels
print "Would you like to add another network? (y/n)"
response = raw_input()
if response.lower() in ["y", "yes"] :
    response = True
else : response = False
while response :
    print "Please give this network a name."    
    networkname = raw_input()
    print "What is the hostname of %s?" % (networkname)
    hostname = raw_input()
    networks[hostname] = {"hostnick":networkname}
    print "What port will you use for %s?" % (hostname)
    port = input()
    networks[hostname]["port"] = port
    print "Do you want the bot to use ssl on this network? (y/n)"
    yesno = raw_input()
    if yesno.lower() in ["yes", "y"] :
        ssl = True
    else : ssl = False
    networks[hostname]["ssl"] = ssl
    print "Do you want the bot to use IPv6 on this network? (y/n)"
    yesno = raw_input()
    if yesno.lower() in ["yes", "y"] :
        ipv6 = True
    else : ipv6 = False
    networks[hostname]["ipv6"] = ipv6
    print "What is your hostname or vhost on this network?"
    vhosts.append(raw_input())
    print "Please type all the channels you want the bot to automatically join when connecting to this network, seperating them with spaces"
    channels = raw_input().split(" ")
    networks[hostname]["channels"] = channels
    print "Would you like to add (another) network? (y/n)"
    response = raw_input()
    if response.lower() in ["y", "yes"] :
        response = True
    else : response = False

print "Now generating conf.py..."
defaultconfig = """hosts = %(hosts)s
ports = %(ports)s
ipv6 = %(ipv6)s
ssl = %(ssl)s
channels = %(channels)s
ident = "sonicbot"
autoreconnect = []
nick = %(nick)s
realname = "sonicbot"
connectcommands = {}
bpass = %(bpass)s
owner = %(owner)s
admin = {owner:%(vhosts)s}
prefix = %(prefix)s
ignorelist = []
debug = False
phpserv = False
staffchannel = {}
welcomechans = []
avchans = []
ai = False
bads = []
mail_url = ""
hostignores = []
twituser = %(twituser)s
twitpass = %(twitpass)s
staffchannel = {}
logdir = "logs"
modeonjoin = {"": [""]}
committracker = False"""
filling = {"vhosts":repr(vhosts), "nick":repr(nick), "owner":repr(owner), "bpass":repr(bpass), "prefix":repr(prefix), "twituser":repr(twituser), "twitpass":repr(twitpass)}
hosts = networks.keys()
ports = [networks[host]["port"] for host in hosts]
ipv6 = [networks[host]["ipv6"] for host in hosts]
ssl = [networks[host]["ssl"] for host in hosts]
filling["hosts"] = repr(hosts)
filling["ports"] = repr(ports)
filling["ipv6"] = repr(ipv6)
filling["ssl"] = repr(ssl)
channels = {}
for host in hosts :
    channels[host] = networks[host]["channels"]
filling["channels"] = repr(channels)
configfile = open("conf.py", "w")
configfile.write(defaultconfig % filling)
configfile.close()
print "Wrote config to file"
print "Generating world.py..."
defaultworld = """connections = {}
hostcount = 0
feeds = {}
relay_channels = []
hostnicks = %s
try :
    import ssl
    pythonversion = "2.6"
except : pythonversion = "2.5"
instances = {}
rconnections = {}
waitfordatastarted = False
conlist = []
"""
hostnicks = {}
for host in hosts :
    hostnicks[host] = networks[host]["hostnick"]
worldfile = open("world.py", "w")
worldfile.write(defaultworld % (repr(hostnicks)))
worldfile.close()
print "Wrote world to file"
print "Looks like we are all done!  To start sonicbot, run the command 'python run.py'.  Have a nice day!"
