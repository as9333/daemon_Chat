import socket,threading
from time import sleep
from os import _exit
from sys import argv
receiver_switch=1
if(len(argv)<3):
    print "[!]Not enough arguments\nUsage:daemon_chat_client <host> <port>"
    _exit(0)
else:
    host=argv[1]
    try:
        target_port=int(argv[2])
    except:
        print "[!]Invalid port\nUsage:daemon_chat_server <host> <port>"
        _exit(0)
try:
    target_ip=socket.gethostbyname(host)
except:
    print "\n[!]Failed to resolve host\nUsage:daemon_chat_client <host> <port>"
    _exit(0)
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    client.connect((target_ip,target_port))
except:
    print "\n[!]Server not reachable\nUsage:daemon_chat_client <host> <port>"
    _exit(0)
print "\n[+]Connected to server on %s:%d"%(target_ip,target_port)
def receiver():
    re=""
    while receiver_switch==1:
        try:
            re=client.recv(4096)
            if(re!=""):
                print re
        except:
            pass
receiver_thread=threading.Thread(target=receiver)
receiver_thread.start()
msg="ready"
while msg.lower()!="/exit":
    msg=raw_input()
    try:
        client.send(msg)
    except:
        print "[!]An error was encountered while sending the message"
receiver_switch=0
client.close()
