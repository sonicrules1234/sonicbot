import time, traceback
minlevel = 1
arguments = ["self", "info"]
keyword = "MODE"

def main(self, info) :
    """This function is called whenever modes are changed"""
    try : 
        mode = info["words"][3]
        modesymbols = {"y":"!", "h":"%", "o":"@", "v":"+", "F":"~", "q":"~", "a":"&"}
        if len(info["words"]) > 4 :
            recvrs = info["words"][4:]
            recvr = 0
            self.logwrite(info["channel"], _("[%(time)s] **%(nick)s set mode %(mode)s on %(nick2)s\n") % dict(time=time.strftime("%b %d %Y, %H:%M:%S %Z"), nick=info["sender"], mode=mode, nick2=" ".join(recvrs)))
            for letter in mode:
                if letter == "+" : modetype = True
                elif letter == "-" : modetype = False
                else :
                    if letter in modesymbols.keys() :
                        if letter == "q" and recvrs[recvr] not in self.channellist[info["channel"]] :
                            pass
                        else :
                            print self.host
                            if modetype :
                                if letter not in self.chanmodes[info["channel"]][recvrs[recvr]] :
                                    self.chanmodes[info["channel"]][recvrs[recvr]].append(modesymbols[letter])
                            elif not modetype :
                                if letter in self.chanmodes[info["channel"]][recvrs[recvr]] :
                                    self.chanmodes[info["channel"]][recvrs[recvr]].remove(letter)
                        recvr += 1
        else :
            self.logwrite(self.nick, _("[%(time)s] **%(nick)s set mode %(mode)s on %(channel)s\n") % dict(time=time.strftime("%b %d %Y, %H:%M:%S %Z"), nick=info["sender"], mode=mode, channel=info["channel"]))
    except :
        traceback.print_exc()
