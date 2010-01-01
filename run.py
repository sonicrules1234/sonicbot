import conf, world, sonicbotv3, thread, time, socket, shelve, simplejson, traceback, urllib
class sonicbotd :
    def onConnect(self, sock, address) :
        self.sock = sock
        self.buffer = ""
        self.address = address[0]
        self.status = {"connected":True}
        print "Receiving from %s" % (self.address)
        if self.address in ["127.1.0.1", "127.0.0.1"] : return self.startLoop()
    def startLoop(self) :
        while self.status["connected"] :
            data = self.sock.recv(4096)
            parsed = self.parseData(data)
        self.sock.close()
        return parsed
    def parseData(self, data) :
        print "[IN %s] %s" % (self.address, data)
        self.status["connected"] = False
        try : json = simplejson.loads(data)
        except :
            traceback.print_exc()
            print data
            json = None
        return json
    

print "Starting..."

botinstance = sonicbotv3.sonicbot()
thread.start_new_thread(botinstance.start, (conf.hosts[world.hostcount], conf.ports[world.hostcount]))
try :
    if conf.committracker :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 9001))
        s.listen(1)
        while True :
            conn, addr = s.accept()
            d = sonicbotd()
            json = d.onConnect(conn, addr)
            try :
                if json != None :
                    commits = shelve.open("commits.db", writeback=True)
                    if not commits.has_key("networks") :
                        commits["networks"] = {}
                        commits.sync()
                    for network in commits["networks"].keys() :
                        for channel in commits["networks"][network].keys() :
                            if json[u"repository"][u"url"].encode("utf-8") in commits["networks"][network][channel] :
                                for commit in json[u"commits"] :
                                    if network in world.connections.keys() : world.connections[network].ircsend(channel, "Commit to %s by %s '%s' %s" % (json[u"repository"][u"name"].encode("utf-8"), commit[u"author"][u"name"].encode("utf-8"), commit[u"message"].encode("utf-8"), urllib.urlopen("http://is.gd/api.php?longurl=" + commit[u"url"].encode("utf-8")).read()))
                    commits.close()
            except : traceback.print_exc()
    else :
        while True :
            time.sleep(5)
except :
    traceback.print_exc()
    for connection in world.connections.keys() :
        world.connections[connection].rawsend("QUIT :Hmm, somebody hit Ctrl-C, better /quit!\n")
        world.connections[connection].cleanup()

print "Shutting down..."
