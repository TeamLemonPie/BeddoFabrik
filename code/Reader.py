class Reader:

	def __init__(self, id, bus, subbus, reset, activated=True):
		self.id = id
		self.bus = bus
		self.subbus = subbus
		self.reset = reset
		self.activated = activated
		self.hold = []

	def isNewCard(self, cardID):
		if len(self.hold) == 2:
			self.activated = False
			return False

		if cardID not in self.hold:
			self.hold.append(cardID)
			return True
		else:
			return False

	def clearHold(self):
		self.hold = []
		self.activated = True

	def clearCardFromHold(self, cardID):
		self.hold.remove(cardID)

	def __str__(self):
		return "[Reader: id={}, bus={}, subbus={}, reset={}, hold={}, activated={}]".format(self.id,
																							self.bus,
																						  	self.subbus,
																						  	self.reset,
																						  	self.hold,
																							self.activated)
