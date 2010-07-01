import time
arguments = ["self", "info"]
keyword = "KICK"
minlevel = 1
def main(self, info) :
    """This function is called whenever somebody gets kicked, including sonicbot himself"""
    recvr = info["words"][3]
    self.logwrite(info["channel"], _("[%(time)s] **%(kicker)s has kicked %(kickee)s from %(channel)s\n") % dict(time=time.strftime("%b %d %Y, %H:%M:%S %Z"), kicker=info["sender"], kickee=recvr, channel=info["channel"]))
    self.channellist[info["channel"]].remove(recvr)
