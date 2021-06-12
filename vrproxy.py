#!/bin/python3


# usefull Links
# http://woodair.net/sbs/article/barebones42_socket_data.htm

import socket
import sys
import time


HELP= sys.argv[0] + " <source address> <source port>"

MSG_ID = 0
MSG_TYPE = 1
MSG_MODES = 4
MSG_LAT = 14
MSG_LONG = 15

g_craft = {}

def log(line):
	parts = line.split(",")
	if parts[MSG_ID] != "MSG":
		print("Unknown message type", parts[MSG_TYPE])
		return False
		
	msgType = int(parts[MSG_TYPE])
	msgModes = parts[MSG_MODES]
	
	#print(parts[MSG_ID],msgType)
	if (msgType == 2) or (msgType == 3):
		# This contains long and lat.
		# print(msgModes," : ", parts[MSG_LONG],",",parts[MSG_LAT])
		g_craft[msgModes] = (parts[MSG_LONG],parts[MSG_LAT])
		return True
	
	if g_craft.get(msgModes) != None:
		return True
		
	print("No location for...",msgModes)
	
	
		
		
def aline(line):
	#print(">>" + line + "<<")
	log(line)

def  proxy(source_address,source_port):
	s = socket.create_connection((source_address,source_port))
	s.setblocking(0)
	buffer = ""
	total_bytes = 0
	timeStart = time.time()
	timePrint = timeStart
	while(True):
		try:
			data = s.recv(200)
			newData = data.decode('utf-8')
			total_bytes = total_bytes + len(newData)
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
				print((total_bytes/(now - timePrint))/1000.0,"kbytes/s")
				timePrint = now
				total_bytes = 0
			pass
	s.close()


if __name__ == "__main__":
	if not (len(sys.argv) == 3):
		print(HELP)
		sys.exit()
	proxy(sys.argv[1],sys.argv[2])


