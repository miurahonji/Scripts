#!/usr/bin/env python

import daemon, socket
import os, sys, time

WORKDIR = '/tmp/python_daemon'
SOCKFILE = os.sep.join([WORKDIR, 'socket.file'])

class ClientDaemon():
	def __init__(self):
		# if os.system('./delegated') == 0:
		# 	print 'sleeping'
		# 	time.sleep(3)
		self.__connect__('Hello world 1!!')
		self.__connect__('Hello world 2!!')

	def __connect__(self, msg):
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.socket.connect(SOCKFILE)
		# Error if send data bigger than 4096
		self.socket.send(msg)

if __name__ == '__main__':
	a = ClientDaemon()
