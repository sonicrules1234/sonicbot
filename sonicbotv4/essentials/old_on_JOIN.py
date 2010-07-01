import time
minlevel = 1
arguments = ["self", "info"]
keyword = "JOIN"
def main(self, info) :
        if self.nick == info["sender"] :
            self.logs[info["channel"]] = open("%s/%s.txt" % (self.networkname, info["channel"]), "a")
            self.channellist[info["channel"]] = []
            self.chanmodes[info["channel"]] = {}
            if info["channel"] in self.users["channels"] :
                if self.users["channels"][info["channel"]]["registered"] :
                    pass
                else :
                    self.enable_all_plugins(info)
            else :
                self.users["channels"][info["channel"]] = {"registered":False, "enabled":[]}

                self.users.sync()
                self.enable_all_plugins(info)
        else :
            if info["sender"] not in self.channellist[info["channel"]] : self.channellist[info["channel"]].append(info["sender"])
        self.chanmodes[info["channel"]][info["sender"]] = []
        self.logwrite(info["channel"], "[%s] ***%s has joined %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["channel"]))
        if info["sender"] == self.nick : self.rawsend("WHO %s\n" % (info["channel"]))
