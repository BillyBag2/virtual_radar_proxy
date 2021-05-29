#!/bin/python3

import socket
import sys


HELP= sys.argv[0] + " <source address> <source port>"


def aline(line):
	print(">>" + line + "<<")


def  proxy(source_address,source_port):
	s = socket.create_connection((source_address,source_port))
	s.setblocking(0)
	buffer = ""
	while(True):
		try:
			data = s.recv(200)
			#print(data)
			buffer = buffer + data.decode('utf-8')
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
			#print('.')
			pass
	s.close()


if __name__ == "__main__":
	if not (len(sys.argv) == 3):
		print(HELP)
		sys.exit()
	proxy(sys.argv[1],sys.argv[2])


