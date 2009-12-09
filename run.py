import conf, world, sonicbotv3, thread, time
botinstance = sonicbotv3.sonicbot()
print "Starting..."
thread.start_new_thread(botinstance.start, (conf.hosts[world.hostcount], conf.ports[world.hostcount]))
try :
    while True :
        time.sleep(5)
except :
    for connection in world.connections.keys() :
        world.connections[connection].rawsend("QUIT :Hmm, somebody hit Ctrl-C, better /quit!\n")
        world.connections[connection].sock.close()
print "Shutting down..."
