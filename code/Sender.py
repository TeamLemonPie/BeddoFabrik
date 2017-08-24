import socket

class Sender:

	def __init__(self, host, port, payload):
		self.host = host
		self.port = port
		self.payload = payload

	def send(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(1)
			s.connect((self.host, self.port))
			s.settimeout(None)
			s.send(self.payload)
			s.close()
			return True
		except:
			print("ERROR: socket timed out, cardID not sent, will retry next time")
			return False