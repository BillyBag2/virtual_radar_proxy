#!/bin/python3

import socket
import sys


HELP= sys.argv[0] + " <source address> <source port>"
def  proxy(source_address,source_port):
	s = socket.create_connection((source_address,source_port))
	s.setblocking(0)
	buffer = ""
	while(True):
		try:
			data = s.recv(10000)
			#print(data)
			buffer = buffer + data.decode('utf-8')
			if(data == b''):
				print("Connction Closed")
				break
			lines = buffer.split("\r\n")
			for line in lines:
				print('>>>\n')
				print(line)
				print('<<<\r')
			buffer = ""
		except socket.error:
        		pass
	s.close()


if __name__ == "__main__":
	if not (len(sys.argv) == 3):
		print(HELP)
		sys.exit()
	proxy(sys.argv[1],sys.argv[2])


