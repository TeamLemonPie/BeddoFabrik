import socket
from Logger import Logger

class ServerDiscover:
	BROADCAST_IP = "255.255.255.255"
	DISCOVER_PORT = 9990
	DISCOVER_RESPONSE_PORT = 9991
	DISCOVER_REQUEST = "DISCOVER_BEDDOMISCHER_REQUEST"
	DISCOVER_RESPONSE = "DISCOVER_BEDDOMISCHER_RESPONSE"

	def __init__(self):
		pass

	def Discover(self):
		Logger.info("Trying to discover BeddoMischer...")
		ip = self.__SendRequest()
		Logger.info("Found BeddoMischer with IP: {}".format(ip))
		return ip

	def __SendRequest(self):
		success = False
		while not success:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
				sock.sendto(self.DISCOVER_REQUEST.encode(), ("<broadcast>", self.DISCOVER_PORT))

				while True:
					data, ip = sock.recvfrom(1024)
					if data.decode() == self.DISCOVER_RESPONSE:
						success = True
						return ip[0]
			except BaseException as e:
				Logger.error(e.__cause__)
