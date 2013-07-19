#!/usr/bin/python

from bluetooth import *
import sys,time

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

bd_addr = "00:50:C2:BA:02:E8" # sys.argv[1]
port = 1

client_sock = BluetoothSocket( RFCOMM )
client_sock.connect((bd_addr, port))

def send_page(fname,num):
	send_line(client_sock,"PAGE "+num)
	time.sleep(1)

	f = open(fname,"r")
	while True:
		page = f.read(8192)
		if len(page) == 0: break
		print "sending %d bytes",len(page)
		client_sock.send(page)
		time.sleep(1)
	f.close()
	client_sock.send(page)

	data = read_line(client_sock)
	print "received [%s]" % data

	send_line(client_sock,"PING")
	time.sleep(1)


try:
	while True:
#		send_line(client_sock,"VIRGIN")
#		data = read_line(client_sock)
#		if len(data) == 0: break
#		print "received [%s]" % data
#		break

		send_line(client_sock,"GETPARTNER")
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data
		time.sleep(1)

		send_line(client_sock,"PARTNER ID=FEFEFEFEFEFEFEFE")
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data
		time.sleep(1)

		send_line(client_sock,"GETBOOKS")
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data
		time.sleep(1)

		send_line(client_sock,"BOOK ID=8000000002DF9301")
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data
		time.sleep(1)

		send_line(client_sock,"TITLE Zm9vYmFyYmF6")
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data
		time.sleep(1)

		send_line(client_sock,"AUTHOR RmxvcmlhbiBFY2h0bGVy")
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data
		time.sleep(1)

		send_page("/home/floe/page0.gz","0")
		send_page("/home/floe/page1.gz","1")
		send_page("/home/floe/page2.gz","2")
		send_page("/home/floe/page3.gz","3")

		send_line(client_sock,"ENDBOOK")
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data
		time.sleep(1)

		send_line(client_sock,"QUIT")
		data = read_line(client_sock)
		if len(data) == 0: break
		print "received [%s]" % data

		break

		'''
		if data == "PING":
			pass
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
			'''

except IOError:
	pass

print "disconnected"
client_sock.close()

