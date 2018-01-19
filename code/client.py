#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import os
import commands
import threading
import time
import subprocess
import logging

PORT=5555
SLOW_IP="10.0.0.3"
FAST_IP="10.1.0.3"

def receiveFromServer(HOST_IP, e):

	global done_receiving
	done_receiving=False
	
	e.wait()
	if done_receiving:
		return

	t_name=threading.current_thread().name	
	
	print t_name + ": starting"
	
	server_address=(HOST_IP,PORT)

	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	file_received=open("received.txt","a")
		
	try:
		
		sock.connect(server_address)
		sock.send(str(file_received.tell()))
		while True:
			if not e.isSet():
				
				file_received.close()
				sock.close()
				
				print t_name + ": waiting"
				e.wait()
	
				file_received=open("received.txt","a")
				
				sock.connect(server_address)
				sock.send(str(file_received.tell()))
				
			data=sock.recv(1024)
			if data:
				file_received.write(data)
				print t_name + ": " + str(file_received.tell())
			else:
				print t_name + ": didn´t receive anything"
				break
	finally:
	
		done_receiving=True	
		file_received.close()
		sock.close()
		print t_name + ": exiting"

if __name__=="__main__":

	e_slow = threading.Event()
	e_fast = threading.Event()
	t_slow = threading.Thread(target=receiveFromServer, args=(SLOW_IP, e_slow))
	t_fast = threading.Thread(target=receiveFromServer, args=(FAST_IP, e_fast))

	t_slow.start()
	t_fast.start()
	
	while True:
		interface_num=commands.getstatusoutput("iwconfig | grep 'ssid' | wc -l")
		print interface_num
		interface_num=interface_num[1][-1:]

		if interface_num=="1": # only slow interface
			print "only the slow AP is in range"	
			e_fast.clear()	
			e_slow.set()

		elif interface_num=="2":
			print "detected a fast AP in range"
			e_slow.clear()
			e_fast.set()
			
		elif interface_num=="0":
			print "no AP is in range"
			e_slow.clear()
			e_fast.clear()

		if (not t_slow.isAlive()) or (not t_fast.isAlive()):
			e_slow.set()
			e_fast.set()
			break;
		
		time.sleep(3)
