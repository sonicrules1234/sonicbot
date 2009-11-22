def main(connection, info, conf) :
    if ":" in info["words"][2] :
        newnick = info["words"][2][1:]
    else : newnick = info["words"][2]
    if newnick.lower().endswith("|pissing") or newnick.lower().endswith("|pissin") :
        print 1
        for channel in connection.channels :
            print channel
            if newnick in connection.channels[channel] :
                print 2
                connection.rawsend("KICK %s %s :TMI\n" % (channel, newnick))
