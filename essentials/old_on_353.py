import time, traceback
minlevel = 1
arguments = ["self", "info"]
keyword = "353"
def main(self, info) :
    """Generates a list of nicks in the channel, also tries to see what modes they have."""
    try :
        for nick in info["words"][5:] :
            if nick != "" :
                correctnick = nick.replace(":", "")
                newnick = nick.replace(":", "")
                for mode in ["!", "%", "@", "&", "~", "+"] :
                    newnick = newnick.replace(mode, "")
                self.chanmodes[info["words"][4].lower()][newnick] = []
                for mode in ["!", "%", "@", "&", "~", "+"] :
                    if mode in correctnick :
                        self.chanmodes[info["words"][4].lower()][newnick].append(mode)
                correctnick = newnick
                self.channellist[info["words"][4].lower()].append(correctnick)
    except : traceback.print_exc()
