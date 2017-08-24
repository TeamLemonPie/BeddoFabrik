import socket
import time

class Connection:

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, host, port):
		retryCount = 0
		while retryCount < 5:
			if self.___connect___(host, port):
				return True
			else:
				retryCount += 1
				print("ERROR - can't connect to {}:{} - Retry {} of 5".format(host, port, retryCount))
				time.sleep(1)
		print("ERROR - can't connect to {}:{} - Giving up after 5 retries".format(host, port, retryCount))
		return False

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
			print("ERROR - can't send, will retry next time")
			return False