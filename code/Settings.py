import json
from Reader import Reader

class Settings:
	def __init__(self):
		with open('config.txt') as f:
			data = f.read()
		data = json.loads(data)
		self.ip = data["ip"]
		self.readers = data["readers"]
		self.server = data["server"]

	def getReaders(self):
		readerList = []
		for reader in self.readers:
			readerList.append(Reader(reader["id"],
									 reader["bus"],
									 reader["subbus"],
									 reader["reset"],
									 reader["activated"]))
		return readerList
