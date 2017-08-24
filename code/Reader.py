class Reader:

	def __init__(self, id, bus, reset):
		self.id = id
		self.bus = bus
		self.reset = reset
		self.hold = []

	def isNewCard(self, cardID):
		if len(self.hold):
			return False

		if cardID not in self.hold:
			self.hold.append(cardID)
			return True
		else:
			return False

	def clearHold(self):
		self.hold = []