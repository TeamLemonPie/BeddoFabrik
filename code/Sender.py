import socket

class Sender:

	def __init__(self, host, port, payload):
		self.host = host
		self.port = port
		self.payload = payload

	def send(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))
		s.send(self.payload)
		s.close()