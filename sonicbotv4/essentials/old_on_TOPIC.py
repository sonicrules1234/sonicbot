import time
arguments = ["self", "info"]
keyword = "TOPIC"
minlevel = 1

def main(self, info) :
    """This function is called whenever somebody somebody changes the topic, including sonicbot himself"""
    self.logwrite(info["channel"], '[%(time)s] **%(nick)s has changed the topic in %(channel)s to "%(topic)s"\n' % dict(time=time.strftime("%b %d %Y, %H:%M:%S %Z"), nick=info["sender"], channel=info["channel"], topic=info["message"]))
