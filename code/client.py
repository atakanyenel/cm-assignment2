#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import os
import commands
import threading
import time
import subprocess

PORT=5555
SLOW_IP="10.0.0.3"
FAST_IP="10.1.0.3"


def receiveFromServer(HOST_IP):
    print "started new thread with %s" % HOST_IP
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   
    server_address=(HOST_IP,PORT)
    sock.connect(server_address)
    file_received=open("received.txt","a")
    file_at_hand=file_received.tell()
    #print file_at_hand
    amount_received=file_at_hand
    sock.send(str(file_at_hand))


    try:
        data=sock.recv(1024)
        while data:
            file_received.write(data)
            amount_received+=len(data)
            print amount_received
            data=sock.recv(1024)
        print file_received.tell()
    finally:
        "closing socket"
        sock.close()
        
        file_received.close()
    
        sys.exit()
if __name__=="__main__":
        if sys.argv[1]=="slow":
            receiveFromServer(SLOW_IP)
        elif sys.argv[1]=="fast":    
            receiveFromServer(FAST_IP)

        elif sys.argv[1]=="local":
            print "local"
            receiveFromServer("localhost")
        elif sys.argv[1]=="main":
            slow_process=subprocess.Popen(["echo","slow"])
            fast_process=subprocess.Popen(["echo","fast"])
            while True:
                interface_num=commands.getstatusoutput("iwconfig |grep 'ssid' | wc -l")#[1][-1:]
                #interface_num=commands.getstatusoutput("echo $[RANDOM%3+1]" )#[1][-1:]
                print interface_num
                interface_num=interface_num[1][-1:]

                if interface_num=="1": # only slow interface
                    print "slow"
                    if int(commands.getstatusoutput("ps aux | grep python | grep slow | wc -l")[1][-1:])>2:
                        #slow process running
                        print "slow process running"
                        pass
                    else:
                        #slow process not running
                        print "starting slow process"
                        commands.getstatusoutput("kill -2 %s"% fast_process.pid)
                        #kill fast process or do nothing
                        if slow_process.poll()==False:
                            slow_process=subprocess.Popen(["python","code/client.py","slow"]) #start slow process
                            print "slow process started"
                elif interface_num=="2":
                    print "fast"
                    if int(commands.getstatusoutput("ps aux | grep python | grep fast | wc -l")[1][-1:])>2:
                        #fast process running
                        pass
                    else:
                        
                        commands.getstatusoutput("kill -2 %s" %slow_process.pid) 
                        #kill slow process or do nothing
                        if fast_process.poll()==False:
                            fast_process=subprocess.Popen(["python","code/client.py","fast"])
                            print "fast process started"
                elif interface_num=="3":
                    print "no_connection"
                    commands.getstatusoutput("kill -2 %s" %fast_process.pid)
                    commands.getstatusoutput("kill -2 %s" %slow_process.pid)

                time.sleep(3)
