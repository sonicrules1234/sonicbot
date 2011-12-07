import time
arguments = ["self", "info"]
keyword = "NICK"
minlevel = 1
def main(self, info) :
    """This function is called whenever somebody /nick's"""
    if ":" in info["words"][2] :
        newnick = info["words"][2][1:]
    else : newnick = info["words"][2]
    self.hostnames[newnick] = info["hostname"]
    self.whoislist[newnick] = info["whois"]
    if not self.debug : print _("[%(time)s]**%(oldnick)s is now known as %(newnick)s") % dict(time=time.strftime("%b %d %Y, %H:%M:%S %Z"), oldnick=info["sender"], newnick=info["words"][2][1:])
    for channel in self.channellist :
        if info["sender"] in self.channellist[channel] :
            self.channellist[channel].remove(info["sender"])
            self.channellist[channel].append(newnick)
            self.chanmodes[channel][newnick] = self.chanmodes[channel][info["sender"]]
            del self.chanmodes[channel][info["sender"]]
            self.logwrite(channel, _("[%(time)s] **%(oldnick)s is now known as %(newnick)s\n") % dict(time=time.strftime("%b %d %Y, %H:%M:%S %Z"), oldnick=info["sender"], newnick=newnick))
