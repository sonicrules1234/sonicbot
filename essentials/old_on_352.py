import time
minlevel = 1
arguments = ["self", "info"]
keyword = "352"
def main(self, info) :
    self.hostnames[info["words"][7]] = info["words"][5]
    self.whoislist[info["words"][7]] = info["words"][7] + "!" + info["words"][4] + "@" + info["words"][5]
