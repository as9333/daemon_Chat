#!usr/bin/env/ python
import socket,threading,Queue,datetime
from time import sleep
from os import _exit
from sys import argv
clients=[]
clientIdPool=0
usernameColor="\033[1;32;40m"#green
timeColor="\033[1;31;40m"#red
resetColor="\033[1;0;0m"
buf=Queue.Queue()
banner="""
  ____       _     U _____ u  __  __    U  ___ u  _   _    
 |  _"\  U  /"\  u \| ___"|/U|' \/ '|u   \/"_ \/ | \ |"|   
/| | | |  \/ _ \/   |  _|"  \| |\/| |/   | | | |<|  \| |>  
U| |_| |\ / ___ \   | |___   | |  | |.-,_| |_| |U| |\  |u  
 |____/ u/_/   \_\  |_____|  |_|  |_| \_)-\___/  |_| \_|   
  |||_    \|    >>  <<   >> <<,-,,-.       \|    ||   |\,-.
 (__)_)  (__)  (__)(__) (__) (./  \.)     (__)   (_")  (_/ 
   ____   _   _      _       _____  
U /"___| |'| |'| U  /"\  u  |_ " _| 
\| | u  /| |_| |\ \/ _ \/     | |   
 | |/__ U|  _  |u / ___ \    /| |\  
  \____| |_| |_| /_/   \_\  u |_|U  
 _// |\  /|   |\  \|    >>  _// |\_ 
(__)(__)(_") ("_)(__)  (__)(__) (__)
-->with love, blackdaemon<--
"""
def client_life(client,addr):
    print "[+]Accepted connection from %s:%d"%(addr[0],addr[1])
    client.send(banner)
    client.send(timeColor+datetime.datetime.now().strftime("%H:%M")+"|"+resetColor+usernameColor+"(0)daemon_chat_server>"+resetColor+"Hi, welcome")
    username="daemon_chat_server"
    while username.lower().strip() in ["daemon_chat_server",""]:
        client.send(timeColor+datetime.datetime.now().strftime("%H:%M")+"|"+resetColor+usernameColor+"(0)daemon_chat_server>"+resetColor+"Enter username to continue")
        username=client.recv(1024)
        if username.lower().strip()=="daemon_chat_server":
            client.send(timeColor+datetime.datetime.now().strftime("%H:%M")+"|"+resetColor+usernameColor+"(0)daemon_chat_server>"+resetColor+"reserved username!")
        elif username.lower().strip()=="":
            client.send(timeColor+datetime.datetime.now().strftime("%H:%M")+"|"+resetColor+usernameColor+"(0)daemon_chat_server>"+resetColor+"invalid username!")
        else:
            client.send(timeColor+datetime.datetime.now().strftime("%H:%M")+"|"+resetColor+usernameColor+"(0)daemon_chat_server>"+resetColor+"Accepted username %s. Send '/exit' to close connection"%(username))
            global clientIdPool
            clientIdPool+=1
            clientId="("+str(clientIdPool)+")"
    buf.put([datetime.datetime.now().strftime("%H:%M"),"(0)daemon_chat_server",clientId+username+" joined"])
    count=0
    while True:
        try:
            msg=client.recv(4096)
            if msg=="":
                if count>100:
                    buf.put([datetime.datetime.now().strftime("%H:%M"),"(0)daemon_chat_server","Connection to "+clientId+username+" was lost!"])
                    clients.remove(tuple([client,addr]))
                    break
                count+=1
                continue
            else:
                buf.put([datetime.datetime.now().strftime("%H:%M"),clientId+username,msg])
        except:
            print "\n[!]An error was encountered while trying to receive.\nclient:"+str(client)+str(addr)
            break
        if msg.lower()=="/exit":
            client.send(timeColor+datetime.datetime.now().strftime("%H:%M")+"|"+resetColor+usernameColor+"(0)daemon_chat_server>"+resetColor+"Closing connection...")
            clients.remove(tuple([client,addr]))
            client.close()
            break
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
if(len(argv)<3):
    print "[!]Not enough arguments!\nUsage:daemon_chat_server <host> <port>"
    _exit(0)
else:
    host=argv[1]
    try:
        bind_port=int(argv[2])
    except:
        print "[!]Invalid port\nUsage:daemon_chat_server <host> <port>"
        _exit(0)
try:
    bind_ip=socket.gethostbyname(host)
except:
    print "\n[!]Failed to resolve host\nUsage:daemon_chat_server <host> <port>"
    _exit(0)
try:
    server.bind((bind_ip,bind_port))
    server.listen(5)
    print "[+]Listening on %s:%d"%(bind_ip,bind_port)
except:
    print "[!]Failed to start server\nUsage:daemon_chat_server <host> <port>"
    _exit(0)
def server_life():
    print "[+]server awake"
    while True:
        client,addr=server.accept()
        clients.append(tuple([client,addr]))
        client_thread=threading.Thread(target=client_life,args=(client,addr))
        client_thread.start()
def lord():
    print "[+]lord awake"
    while True:
        if len(clients)==0:
            sleep(30)
            if len(clients)==0:
                print "[!]No clients joined...stopping server."
                server.shutdown(socket.SHUT_RDWR)
                server.close()
                _exit(0)
def broadcast():
    print "[+]broadcast awake"
    while True:
        while not buf.empty():
            each_msg=buf.get()
            for c in clients:
                try:
                    c[0].send(timeColor+each_msg[0]+"|"+resetColor+usernameColor+each_msg[1]+">"+resetColor+each_msg[2])
                except:
                    print "\n[!]An error was encountered while trying to broadcast.\nclient:"+str(c)
lord_thread=threading.Thread(target=lord)
server_thread=threading.Thread(target=server_life)
broadcast_thread=threading.Thread(target=broadcast)
banner1="""
  ____       _     U _____ u  __  __    U  ___ u  _   _    
 |  _"\  U  /"\  u \| ___"|/U|' \/ '|u   \/"_ \/ | \ |"|   
/| | | |  \/ _ \/   |  _|"  \| |\/| |/   | | | |<|  \| |>  
U| |_| |\ / ___ \   | |___   | |  | |.-,_| |_| |U| |\  |u  
 |____/ u/_/   \_\  |_____|  |_|  |_| \_)-\___/  |_| \_|   
  |||_    \|    >>  <<   >> <<,-,,-.       \|    ||   |\,-.
 (__)_)  (__)  (__)(__) (__) (./  \.)     (__)   (_")  (_/ 
   ____   _   _      _       _____  
U /"___| |'| |'| U  /"\  u  |_ " _| 
\| | u  /| |_| |\ \/ _ \/     | |   
 | |/__ U|  _  |u / ___ \    /| |\  
  \____| |_| |_| /_/   \_\  u |_|U  
 _// |\  //   |\  \|    >>  _// |\_ 
(__)(__)(_") ("_)(__)  (__)(__) (__)

  ____   U _____ u   ____   __     __ U _____ u   ____    
 / __"| u\| ___"|/U |  _"\ u\ \   /"/u\| ___"|/U |  _"\ u 
<\___ \/  |  _|"   \| |_) |/ \ \ / //  |  _|"   \| |_) |/ 
 u___) |  | |___    |  _ <   /\ V /_,-.| |___    |  _ <   
 |____/>> |_____|   |_| \_\ U  \_/-(_/ |_____|   |_| \_\  
  )(  (__)<<   >>   //   |\_  //       <<   >>   //   |\_ 
 (__)    (__) (__) (__)  (__)(__)     (__) (__) (__)  (__)
-->with love, blackdaemon<--
"""
print banner1
print "Default timeout: 30 seconds"
broadcast_thread.start()
server_thread.start()
lord_thread.start()
print "Type 'stop' to stop server"
while True:
    cmd=raw_input()
    if cmd.strip().lower()=="stop":
        print "[+]Stopping server..."
        server.shutdown(socket.SHUT_RDWR)
        server.close()
        _exit(0)
    else:
        print "[!]Type 'stop' to stop server"
#def dbug():
#    """debug mode"""
#    while True:
#        print "\nINFO-->"
#        print "clients"
#        print clients       
#        print "\nno. of threads: "
#        print len(threading.enumerate())
#        sleep(5)
#dbug_thread=threading.Thread(target=dbug)
#dbug_thread.start()
