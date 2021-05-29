#!/bin/python3


import socket

s = socket.create_connection(('51.38.80.19',33001))

while(True):
	data = s.recv(10)
	print(data)

	if(data == b''):
		print("Connction Closed")
		break

s.close()


