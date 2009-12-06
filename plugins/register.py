import shelve, time, hashlib, random, string
arguments = ["self", "info", "args", "conf"]
minlevel = 4
helpstring = "register <nick>"
def main(connection, info, args, conf) :
    mail = shelve.open("mail.db")
    timet = str(int(time.time()))
    temp = {}
    password = ""
    for letter in range(6) :
        password += random.choice(string.letters)
    temp["hostname"] = [connection.nicks[args[1]]]
    temp["password"] = hashlib.sha512(password).hexdigest()
    temp["messages"] = {}
    temp["userorder"] = ["SonicMail"]
    temp["notify"] = True
    temp["messages"]["SonicMail"] = {}
    temp["messages"]["SonicMail"]["msgorder"] = [[timet, True]]
    temp["messages"]["SonicMail"][timet] = "Welcome to SonicMail!  To send mail using IRC, use ';mail <recipient> <message>'.  To check your mail through IRC, use the ;mcheck command.  Help for the ;mcheck command can be found by using ';mcheck help'."
    mail[args[1].replace("[", "").replace("]", "")] = temp
    mail.sync()
    mail.close()
    connection.ircsend(info["channel"], "%s is now registered." % (args[1]))
    connection.ircsend(args[1], "You can now login to your mail at %s Your username is '%s' and your password is '%s'.  You may change your password once you have logged in." % (conf.mail_url, args[1].replace("[", "").replace("]", ""), password))
