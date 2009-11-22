#!/usr/bin/env python
import cgi, cgitb, glob, time, os, Cookie, hashlib, shelve, bbcode
form = cgi.FieldStorage()

def cookiecheck() :
    if 'HTTP_COOKIE' in os.environ :
        c = os.environ['HTTP_COOKIE']
        c = c.split('; ')
        handler = {}
        for cookie in c :
            cookie = cookie.split("=")
            handler[cookie[0]] = cookie[1]
        return handler
handler = cookiecheck()

def printuserlist() :
    mail = shelve.open("/home/sonicrules1234/sonicbot-freenode/mail.db")
    print "Content-Type: text/html\n"
    print """<html>
<head>
<title>User list</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />"""
    for user in mail.keys() :
        print '<p><a href="index.py?action=sendform&amp;senduser=%s">%s</a></p>' % (user, user)
    mail.close()
    print '<p><a href="index.py">Back</a></p>'
    print """<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>\n</body>
</html>"""

def sendmessage(handler, forms) :
    mail = shelve.open("/home/sonicrules1234/sonicbot-freenode/mail.db", writeback=True)
    print "Content-Type: text/html\n"
    if mail.has_key(forms["senduser"].value) :
        if not mail[forms["senduser"].value]["messages"].has_key(handler["username"]) :
            mail[forms["senduser"].value]["messages"][handler["username"]] = {}
            mail[forms["senduser"].value]["userorder"].append(handler["username"])
            mail.sync()
            mail[forms["senduser"].value]["messages"][handler["username"]]["msgorder"] = []
            mail.sync()
        if len(mail[forms["senduser"].value]["messages"][handler["username"]].keys()) < 10 :
            timet = str(int(time.time()))
            mail[forms["senduser"].value]["messages"][handler["username"]][timet] = forms["message"].value
            mail.sync()
            mail[forms["senduser"].value]["messages"][handler["username"]]["msgorder"].append([timet, True])
            mail[forms["senduser"].value]["notify"] = True
            mail.sync()
            print """<html>
<head>
<title>Message Sent</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<p>You message was sent successfully.</p>
<p><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""
        else : """<html>
<head>
<title>Too many messages</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<p>You have already sent 10 messages to this person, so they must delete some before you can send any more to them.</p>
<p><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""
    else :
        print """<html>
<head>
<title>Error</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<p>No such user exists in my database.</p>
<p><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""
    mail.close()

def printsendform(forms) :
    if forms.has_key("senduser") : senduser = forms["senduser"].value
    else : senduser = ""
    print "Content-Type: text/html\n"
    print """<html>
<head>
<title>Send a message</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<form name="input" action="index.py" method="post">
User to send this message:<br />"""
    print '<input type="text" name="senduser" value="%s" />' % (senduser)
    print """<br />Message: <br />
<textarea rows="10" cols="40" name="message"></textarea>
<br />
<input type="hidden" name="action" value="send" />
<input type="submit" value="Submit" />
</form>
<br />
<p><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""
    
def loginform() :
    print "Content-Type: text/html\n"
    print """<html>
<head>
<title>Login</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<form name="input" action="index.py" method="post">
User name
<input type="text" name="username" />
<br />
Password:
<input type="password" name="password" />
<input type="submit" value="Submit">
</form>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""


def auth1(forms) :
    mail = shelve.open("/home/sonicrules1234/sonicbot-freenode/mail.db")
    if mail.has_key(forms["username"].value) :
        if mail[forms["username"].value]["password"] == hashlib.sha512(forms["password"].value).hexdigest() :
            mail.close()
            return True
        else :
            print "Content-Type: text/html\n"
            print """<html>
<head>
<title>Invalid</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<p>Invalid username or password<br /><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""
        
            mail.close()
            return False
    else :
        print "Content-Type: text/html\n"
        print """<html>
<head>
<title>Invalid</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<p>Invalid username or password<br /><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""

def auth2(handler) :
    mail = shelve.open("/home/sonicrules1234/sonicbot-freenode/mail.db")
    if mail.has_key(handler["username"]) :
        if mail[handler["username"]]["password"] == handler["password"] :
            mail.close()
            return True
        else :
            mail.close()
            print "Content-Type: text/html\n"
            print """<html>
<head>
<title>Invalid</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<p>Invalid username or password<br /><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""
            return False
    else : 
        print "Content-Type: text/html\n"
        print """<html>
<head>
<title>Invalid</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<p>Invalid username or password<br /><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""
        mail.close()
def deletemail(forms, handler) :
    mail = shelve.open("/home/sonicrules1234/sonicbot-freenode/mail.db", writeback=True)
    del mail[handler["username"]]["messages"][forms["pid"].value][forms["tid"].value]
    mail[handler["username"]]["messages"][forms["pid"].value]["msgorder"].remove([forms["tid"].value, False])
    mail.sync()
    if mail[handler["username"]]["messages"][forms["pid"].value]["msgorder"] == [] :
        del mail[handler["username"]]["messages"][forms["pid"].value]["msgorder"]
        mail.sync()
    if mail[handler["username"]]["messages"][forms["pid"].value] == {} :
        del mail[handler["username"]]["messages"][forms["pid"].value]
        mail[handler["username"]]["userorder"].remove(forms["pid"].value)
        mail.sync()
    mail.close()
    printmail(handler["username"])

def printmail(user) :
    mail = shelve.open("/home/sonicrules1234/sonicbot-freenode/mail.db", writeback=True)
    mail[user]["notify"] = False
    print "Content-Type: text/html\n"
    print "<html>\n<head>\n<title>%s's mail</title>\n</head>\n<body>" % (user)
    print '<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />'
    print '<p><a href="index.py?action=logout">Logout</a> <a href="index.py"/>Check Mail</a> <a href="index.py?action=userlist">User List</a></p>'
    for sender in mail[user]["messages"].keys() :
        for message in range(len(mail[user]["messages"][sender]["msgorder"])) :
            mail[user]["messages"][sender]["msgorder"][message][1] = False
        if mail[user]["messages"][sender] != {} :
            print "<h4>%s said:</h4>\n<ul>" % (sender)
            for message in mail[user]["messages"][sender].keys() :
                if message != "msgorder" :
                    try : print '<li>[%s] %s\n<ul>\n<a href="index.py?action=delete&pid=%s&tid=%s">Delete this message</a>\n ' % (time.strftime("%x %X %Z", time.gmtime(int(message))), bbcode.render_bbcode(mail[user]["messages"][sender][message]), sender, message)
                    except : print '<li>[%s] This message was invalid\n<ul>\n<a href="index.py?action=delete&pid=%s&tid=%s">Delete this message</a>\n ' % (time.strftime("%x %X %Z", time.gmtime(int(message))), sender, message)
                    if sender in mail.keys() : print '<a href="index.py?action=sendform&amp;senduser=%s">Reply</a>' % (sender)
                    print '</ul>\n</li>'

            print "</ul>"
    print '<p><a href="index.py?action=passform">Change your password</a></p>'
    print '<p><a href="index.py?action=sendform">Send a message</a></p>'
    print """<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>"""
    print "</body>\n</html>"
    mail.close()

def printpassform(handler) :
    print "Content-Type: text/html\n"
    print """<html>
<head>
<title>Login</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<form name="input" action="index.py" method="post">
New Password:
<input type="password" name="newpassword" />
<input type="hidden" name="action" value="changepass">
<input type="submit" value="Submit">
</form>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""
    
def changepass(handler, forms) :
    mail = shelve.open("/home/sonicrules1234/sonicbot-freenode/mail.db")
    temp = mail[handler["username"]]
    temp["password"] = hashlib.sha512(forms["newpassword"].value).hexdigest()
    mail[handler["username"]] = temp
    mail.sync()
    mail.close()
    c = Cookie.SimpleCookie()
    c["password"] = hashlib.sha512(forms["newpassword"].value).hexdigest()
    print c
    print "Content-Type: text/html\n"
    print """<html>
<head>
<title>Password Change Complete</title>
</head>
<body>
<img style="text-align:center" src="logo.png" alt="sonicbot mail logo" />
<p>Password was changed successfully</p>
<p><a href="index.py">Back</a></p>
<p style="text-align:center">Interface by sonicrules1234 | Logo inspired by wgsilkie's old logo</p>
</body>
</html>"""


if handler == None :
    c = Cookie.SimpleCookie()
    c['sonicbot-mail-status'] = "out"
    print c
    loginform()
elif "sonicbot-mail-status" in handler :
    if form.has_key("username") and form.has_key("password") :                
        if auth1(form) :
            c = Cookie.SimpleCookie()
            c['sonicbot-mail-status'] = "in"
            c['username'] = form["username"].value
            c["password"] = hashlib.sha512(form["password"].value).hexdigest()
            print c
            printmail(form["username"].value)
    elif form.has_key("action") :
        if form["action"].value == "logout" :
            if auth2(handler) :
                c = Cookie.SimpleCookie()
                c['sonicbot-mail-status'] = "out"
                print c
                loginform()
        elif form["action"].value == "delete" :
            if form.has_key("pid") and form.has_key("tid") :
                if auth2(handler) :
                    deletemail(form, handler)
        elif form["action"].value == "passform" :
            if auth2(handler) :
                printpassform(handler)
        elif form["action"].value == "changepass" and form.has_key("newpassword") :
            if auth2(handler) :
                changepass(handler, form)
        elif form["action"].value == "sendform":
            if auth2(handler) :
                printsendform(form)
        elif form["action"].value == "send" :
            if auth2(handler) :
                sendmessage(handler, form)
        elif form["action"].value == "userlist" :
            printuserlist()
    elif handler["sonicbot-mail-status"] == "out" : loginform()
    elif handler["sonicbot-mail-status"] == "in":
        if auth2(handler) :
            printmail(handler["username"])
