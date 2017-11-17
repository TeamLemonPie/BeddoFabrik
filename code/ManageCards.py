class ManageCards:

	cards = {}
	
	# Piek
	cards["154-98-11-133-218"] = "1"
	cards["64-91-169-137-59"] = "2"
	cards["46-245-168-137-250"] = "3"
	cards["198-241-168-137-22"] = "4"
	cards["127-72-227-41-253"] = "5"
	cards["78-4-170-137-105"] = "6"
	cards["119-174-226-41-18"] = "7"
	cards["98-155-250-41-42"] = "8"
	cards["1-112-169-137-81"] = "9"
	cards["26-171-169-137-145"] = "10"
	cards["167-132-229-41-239"] = "11"
	cards["150-234-168-137-93"] = "12"

	def getCardFromUID(self, uid):
		try:
			return self.cards[uid]
		except KeyError:
			return None
