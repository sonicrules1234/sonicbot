minlevel = 1
arguments = ["self", "info"]
keyword = "NICK"
def main(self, info) :
    if info["words"][2].startswith(":") :
        newnick = info["words"][2][1:]
    else : newnick = info["words"][2]
    if info["sender"] == self.nick :
        self.nick = newnick
