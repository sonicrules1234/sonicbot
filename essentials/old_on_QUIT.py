import time
arguments = ["self", "info"]
keyword = "QUIT"
minlevel = 1
def main(self, info) :
    """This function is called whenever somebody quits, but not when sonicbot quits"""
    quitmessage = " ".join(info["words"][2:])[1:]
    for channel in self.channellist :
        if info["sender"] in self.channellist[channel] :
            self.channellist[channel].remove(info["sender"])
            self.logwrite(channel, _("[%(time)s] ***%(nick)s has quit (%(reason)s)\n") % dict(time=time.strftime("%b %d %Y, %H:%M:%S %Z"), nick=info["sender"], reason=quitmessage))
            if info["sender"] == self.nick : self.logs[channel].close()
