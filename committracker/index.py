#!/usr/bin/env python
import cgi, cgitb, socket
cgitb.enable()
form = cgi.FieldStorage()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.1.0.1", 9001))
sock.send(form["payload"].value)
sock.close()
print "Content-Type: text/html\n"
print "Worked"
