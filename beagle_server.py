#!/usr/bin/python
# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",1))
server_sock.listen(1)

def read_line(s):
	ret = ''
	while True:
		c = s.recv(1)
		if c == '\n' or c == '':
			break
		else:
			ret += c
	return ret

def send_line(s,line):
	s.send(line+"\n")
	print "sending [%s]" % line

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805F9B34FB"

advertise_service( server_sock, "SampleServer",
  service_id = uuid,
	service_classes = [ uuid, SERIAL_PORT_CLASS ],
	profiles = [ SERIAL_PORT_PROFILE ],
#	protocols = [ OBEX_UUID ]
)
				   
print "Waiting for connection on RFCOMM channel %d" % port

ID="ID=AE37B7881B76AA96"

while True:

	client_sock, client_info = server_sock.accept()
	print "Accepted connection from ", client_info

	try:
		while True:
			data = read_line(client_sock)
			if len(data) == 0: break
			print "received [%s]" % data
			if data == "PING":
				pass
			if data == "VIRGIN":
				send_line(client_sock,"VIRGINOK")
			if data == "GETPARTNER":
				if ID == "":
					send_line(client_sock,"NOPARTNER")
				else:
					send_line(client_sock,"PARTNER "+ID)
			if data.startswith("PARTNER "):
				send_line(client_sock,"PARTNEROK")
				ID=data.split(" ")[1]
			if data == "INFO":
				send_line(client_sock,"PROTOCOL VERSION=8\nFIRMWARE ID=Beagle-F-U BUILDDATE=18.April.2013 GIT=cf3dc863 IAP=0 BLUETOOTH=u.3\nDEVICE SERIAL=3266970344 BDADDR=74:E5:43:51:D4:FA DISPLAY=V110\nVCOM VALUE=1910\nSDCONTENT REVISION=2\nOPTION LOWFLASH=0 FFTBT=1\nINFOOK")
			if data == "MEMORY":
				send_line(client_sock,"BOOKS USE=1 MAXIMUM=15\nCLUSTERS USE=21 MAXIMUM=255 SIZE=59\nMEM TOTAL=8192 FREE=2168\nMEMORYOK")
			if data == "GETBOOKS":
				send_line(client_sock,"BOOK ID=1111111111111111 FIRSTPAGE=1 LASTPAGE=19 CURRENTPAGE=8 AUTHOR=dHh0ciBiZWFnbGU TITLE=S3VyemFubGVpdHVuZw\nGETBOOKSOK")
			if data.startswith("BOOK "):
				send_line(client_sock,"BOOKOK")
			if data.startswith("TITLE "):
				send_line(client_sock,"TITLEOK")
			if data.startswith("AUTHOR "):
				send_line(client_sock,"AUTHOROK")
			if data.startswith("DELETEBOOK "):
				send_line(client_sock,"DELETEBOOKOK")
			if data.startswith("PAGE "):
				while True:
					page = client_sock.recv(8192)
					print "got %d bytes" % len(page)
					f = open(data,"ab") #,"utf-8")
					f.write(page)
					f.close()
					if len(page) < 990:
						break
				send_line(client_sock,"PAGEOK")

	except IOError:
		pass

	print "disconnected"

	client_sock.close()

server_sock.close()
print "all done"

