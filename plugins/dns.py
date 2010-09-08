import commands
arguments = ["self", "info", "args"]
helpstring = "dns <IP or domain name>"
minlevel = 1

def main(connection, info, args) :    
    """Displays the path of the dns of the specified host"""
    connection.ircsend(info["channel"], lookup(args[1]))

def lookup(data, v=4) :
    """This code is not by me.  It was written by nathan from ClueNet"""
    (ov,v)=(v,{4:2,6:10}[v])
    import socket
    data=[data]
    try:
        while True :
            if len(data) > 2 :
                if data[-1] == data[-3] :
                    break
                else :
                    data.append([cur[4][0] for cur in socket.getaddrinfo(data[-1],None) if cur[0]==v][0])
                    if data[-1]==data[-2]: data.pop(-1)
                if data[-1] == data[-3] : break
                else : data.append(socket.gethostbyaddr(data[-1])[0])
            else :
                data.append([cur[4][0] for cur in socket.getaddrinfo(data[-1],None) if cur[0]==v][0])
                if data[-1]==data[-2]: data.pop(-1)
                data.append(socket.gethostbyaddr(data[-1])[0])
    except: pass
    return ['Error resolving %s using IPv%d.'%(data[0],ov)," -> ".join(data)][len(data)>1]

