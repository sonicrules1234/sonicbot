import time
minlevel = 1
arguments = ["self", "info"]
keyword = "PRIVMSG"
def main(self, info) :
        """This function gets called whenever sonicbot receives data with the PRIVMSG commdand from the server.  This includes PM's and any talking in the channels"""
        if not info["message"]: return
        if not info["channel"].startswith("#") :
            if info["channel"] in self.users["channels"] :
                if self.users["channels"][info["channel"]]["registered"] :
                    pass
                else :

                    self.enable_all_plugins(info)
            else :
                self.users["channels"][info["channel"]] = {"registered":False, "enabled":[]}

                self.users.sync()
                self.enable_all_plugins(info)
        if info["channel"] in self.channellist : self.logwrite(info["channel"], "[%s] <%s> %s\n" % (time.strftime("%b %d %Y, %H:%M:%S %Z"), info["sender"], info["message"]))
