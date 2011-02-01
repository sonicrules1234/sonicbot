import time
arguments = ["self", "info"]
keyword = "PART"
minlevel = 1
def main(self, info) :
    """This function is called whenever somebody parts the channel, including sonicbot himself"""
    self.logwrite(info["channel"], _("[%(time)s] ***%(nick)s has parted %(channel)s\n") % dict(time=time.strftime("%b %d %Y, %H:%M:%S %Z"), nick=info["sender"], channel=info["channel"]))
    if self.nick == info["sender"] :
        self.logs[info["channel"]].close()
        del self.channellist[info["channel"]]
        del self.chanmodes[info["channel"]]
    else :
        if info["sender"] in self.channellist[info["channel"]] : self.channellist[info["channel"]].remove(info["sender"])
