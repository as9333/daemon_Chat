import socket
import threading
from time import sleep
receiver_switch=1
target_ip=socket.gethostbyname(raw_input("Host:"))
target_port=input("Port:")
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    client.connect((target_ip,target_port))
except:
    print "\n[!]Server not reachable."
    exit()
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
