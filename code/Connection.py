import socket
import time
from Logger import Logger

class Connection:

	active = True

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, host, port):
		Logger.info("Trying to connect to {}:{}...".format(host, port))
		retryCount = 0
		while self.active:
			if self.___connect___(host, port):
				self.active = False
				Logger.info("Connection established.")
				return True
			else:
				retryCount += 1
				Logger.error("can't connect to {}:{} - Retry {}".format(host, port, retryCount))
				time.sleep(1)

	def ___connect___(self, host, port):
		try:
			self.socket.settimeout(1)
			self.socket.connect((host, port))
			self.socket.settimeout(None)
			return True
		except socket.error:
			return False

	def close(self):
		self.socket.close()

	def send(self, payload):
		try:
			self.socket.send(payload)
			return True
		except:
			return False

	def read(self):
		return self.socket.recv(1024)