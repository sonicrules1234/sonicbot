import os
arguments = ["self", "info", "args"]
minlevel = 5
helpstring = "restart"
def main(connection, info, args) :
    os.popen2('echo "python sonicbot-v3.py" | at now + 1 minutes')
    connection.rawsend("QUIT :Leaving...\n")
