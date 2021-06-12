#!/bin/python3


# usefull Links
# http://woodair.net/sbs/article/barebones42_socket_data.htm

import socket
import sys
import time
import threading


HELP= sys.argv[0] + " <source address> <source port>"

MSG_ID    = 0
MSG_TYPE  = 1
MSG_MODES = 4
MSG_ALT   = 11
MSG_LAT   = 14
MSG_LONG  = 15

g_craft = {}
g_bytesTotal = 0
g_bytesFiltered = 0
g_lock = threading.Lock()
g_clients = []

def hasAlt(n):
	return (n == 2) or (n == 3) or (n == 5) or (n == 6) or (n == 7)
	
def log(line):
	parts = line.split(",")
	if parts[MSG_ID] != "MSG":
		print("Unknown message type", parts[MSG_TYPE])
		return False
		
	msgType = int(parts[MSG_TYPE])
	msgModes = parts[MSG_MODES]
	
	if hasAlt(msgType):
		alt = int(parts[MSG_ALT])
		#if (alt > 50000):
			#print(line)
	
	#print(parts[MSG_ID],msgType)
	if (msgType == 2) or (msgType == 3):
		# This contains long and lat.
		# print(msgModes," : ", parts[MSG_LONG],",",parts[MSG_LAT])
		g_craft[msgModes] = (parts[MSG_LONG],parts[MSG_LAT])
		return True
	
	if g_craft.get(msgModes) != None:
		return True
		
	#print("No location for...",msgModes)
	
def addClient(clientsocket):
	print("addClient")
	with g_lock:
		g_clients.append(clientsocket)
	
	
def getParams(clientsocket):
	print("getParams")
	# TODO: Get location from client.
	addClient(clientsocket)
	

# none blocking funtion to start a thread to read parames from socket
def startGetParams(clientsocket):
	print("startGetParams")
	thread = threading.Thread(target=getParams, args=(clientsocket,))
	thread.start()
	

# Listen for incomming connections.
def listener(port):
	print("listener",port,socket.gethostname())
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((socket.gethostname(), port))
	serversocket.listen(5)
	while True:
		print("accept")
		(clientsocket, address) = serversocket.accept()
		startGetParams(clientsocket)
		
# None blocking start listener.	 	
def startListener(port):
	print("startListener",port)
	thread =threading.Thread(target = listener, args=(port,))
	thread.start()
	
	
def aline(line):
	global g_bytesFiltered
	global g_bytesTotal
	g_bytesTotal = g_bytesTotal + len(line)
	if log(line):
		g_bytesFiltered =g_bytesFiltered + len(line)
	

def  proxy(source_address,source_port):
	global g_bytesFiltered
	global g_bytesTotal
	
	# incoming data socket
	s = socket.create_connection((source_address,source_port))
	s.setblocking(0)
	
	# Start listener for clients
	startListener(50000)
	
	buffer = ""
	timeStart = time.time()
	timePrint = timeStart
	while(True):
		try:
			data = s.recv(200)
			newData = data.decode('utf-8')
			buffer = buffer + newData
			if(data == b''):
				print("Connction Closed")
				break
			lines = buffer.splitlines(True)
			for line in lines[:-1]:
				aline(line)
			#print(len(lines))
			last = lines[-1]
			if last.endswith("\r\n"):
				aline(last)
				buffer = ""
				#print("+++++++")
			else:
				# Last line is only partial.
				buffer = lines[-1]
				#print('************************' + buffer)
		except socket.error:
			now = time.time()
			if now - timePrint > 10.0:
				print((g_bytesTotal/(now - timePrint))/1000.0,"kbytes/s")
				print((g_bytesFiltered/(now - timePrint))/1000.0,"kbytes/s")
				timePrint = now
				g_bytesTotal = 0
				g_bytesFiltered =0
			pass
	s.close()


if __name__ == "__main__":
	if not (len(sys.argv) == 3):
		print(HELP)
		sys.exit()
	proxy(sys.argv[1],sys.argv[2])


