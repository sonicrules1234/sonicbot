import shelve, time, hashlib, random, string
arguments = ["self", "info", "args"]
minlevel = 4
helpstring = "register <nick>"
def main(connection, info, argsf) :
    """Registers a nick to sonicmail"""
    mail = shelve.open("mail.db")
    timet = str(int(time.time()))
    temp = {}
    password = ""
    for letter in range(6) :
        password += random.choice(string.letters)
    temp["hostname"] = [connection.msg[args[1]]]
    temp["password"] = hashlib.sha512(password).hexdigest()
    temp["messages"] = {}
    temp["userorder"] = ["SonicMail"]
    temp["notify"] = True
    temp["messages"]["SonicMail"] = {}
    temp["messages"]["SonicMail"]["msgorder"] = [[timet, True]]
    temp["messages"]["SonicMail"][timet] = _("Welcome to SonicMail!  To send mail using IRC, use ';mail <recipient> <message>'.  To check your mail through IRC, use the ;mail command.  Help for the ;mail command can be found by using ';mail help'.")
    mail[args[1].replace("[", "").replace("]", "")] = temp
    mail.sync()
    mail.close()
    connection.msg(info["channel"], _("%(nick)s is now registered.") % dict(nick=args[1]))
    connection.notice(args[1], _("You can now login to your mail at %(url)s Your username is '%(username)s' and your password is '%(password1)s'.  You may change your password once you have logged in.") % dict(url=self.mail_url, username=args[1].replace("[", "").replace("]", ""), password1=password))
