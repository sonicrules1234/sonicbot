import conf, world, sonicbotv3, thread, time
botinstance = sonicbotv3.sonicbot()
print "Starting..."
thread.start_new_thread(botinstance.start, (conf.hosts[world.hostcount], conf.ports[world.hostcount]))
while True :
    time.sleep(5)
print "Shutting down..."
