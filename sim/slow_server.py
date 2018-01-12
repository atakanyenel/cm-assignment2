from socket import *
import threading
import time
import sys
import os
HOST = ''   # or 127.0.0.1 or localhost
PORT = 5555
ADDR = (HOST,PORT)
BUFFER = 4096

#create a socket (SRV)
#see python docs for socket for more info

srv = socket(AF_INET,SOCK_STREAM)
srv.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
#bind socket to address
srv.bind((ADDR))	#double parens create a tuple with one object
srv.listen(5) # maximum queued connections is 5

print "listening on {}.{}".format(HOST,PORT)

def handle_client(client_socket):
    file_to_send=open("big.txt")
    file_size=os.path.getsize("big.txt")
    start_from=client_socket.recv(8)
    print int(start_from)
    print int(start_from),"/", file_size
    if int(start_from)>file_size:
        print "file already ended"
        file_to_send.close()
    else:
        file_to_send.seek(int(start_from))
        l=file_to_send.read(1024)
    
        while(l):
        #print "sending"
       # time.sleep(0)
            client_socket.send(l)
            time.sleep(0.2)
            l=file_to_send.read(1024)
        file_to_send.close()
while True:
    try:
        conn,addr = srv.accept() #accepts the connection
        print '...connected!'
        handle_client(conn)
        conn.close()
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "client failed"
        conn.close()


