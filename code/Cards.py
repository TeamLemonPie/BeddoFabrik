class Cards:

	cards = {}
	# DEBUG:
	cards["106-31-8-133-248"] = "Pi-7"
	cards["154-98-11-133-118"] = "He-A"
	# TODO fill all cards

	def getCardFromUID(self, uid):
		try:
			return self.cards[uid]
		except KeyError:
			return None
