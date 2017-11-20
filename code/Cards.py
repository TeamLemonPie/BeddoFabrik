class Cards:

	cards = {}
	
	# Pik
	cards["136-4-120-152-108"] = "Pi-2"
	cards["136-4-131-152-151"] = "Pi-3"
	cards["136-4-167-140-167"] = "Pi-4"
	cards["136-4-144-152-132"] = "Pi-5"
	cards["136-4-157-152-137"] = "Pi-6"
	cards["136-4-1-170-39"] = "Pi-7"
	cards["136-4-119-152-99"] = "Pi-8"
	cards["136-4-38-151-61"] = "Pi-9"
	cards["136-4-9-115-246"] = "Pi-10"
	cards["136-4-72-140-72"] = "Pi-B"
	cards["136-4-129-185-180"] = "Pi-D"
	cards["136-4-94-155-73"] = "Pi-K"
	cards["136-4-100-183-95"] = "Pi-A"

	# Herz
	cards["136-4-223-116-39"] = "He-2"
	cards["136-4-105-65-164"] = "He-3"
	cards["136-4-12-84-212"] = "He-4"
	cards["136-4-200-116-48"] = "He-5"
	cards["136-4-199-116-63"] = "He-6"
	cards["136-4-85-182-111"] = "He-7"
	cards["136-4-61-64-241"] = "He-8"
	cards["136-4-86-59-225"] = "He-9"
	cards["136-4-49-64-253"] = "He-10"
	cards["136-4-84-140-84"] = "He-B"
	cards["136-4-98-140-98"] = "He-D"
	cards["136-4-70-164-110"] = "He-K"
	cards["136-4-59-124-203"] = "He-A"

	# Karo
	cards["136-4-147-172-179"] = "Ka-2"
	cards["136-4-72-181-113"] = "Ka-3"
	cards["136-4-62-181-7"] = "Ka-4"
	cards["136-4-11-79-200"] = "Ka-5"
	cards["136-4-49-181-8"] = "Ka-6"
	cards["136-4-86-67-153"] = "Ka-7"
	cards["136-4-66-142-64"] = "Ka-8"
	cards["136-4-56-159-43"] = "Ka-9"
	cards["136-4-28-142-30"] = "Ka-10"
	cards["136-4-12-124-252"] = "Ka-B"
	cards["136-4-11-124-251"] = "Ka-D"
	cards["136-4-81-164-121"] = "Ka-K"
	cards["136-4-133-177-184"] = "Ka-A"

	# Kreuz
	cards["136-4-113-151-106"] = "Kr-2"
	cards["136-4-128-143-131"] = "Kr-3"
	cards["136-4-103-122-145"] = "Kr-4"
	cards["136-4-190-150-164"] = "Kr-5"
	cards["136-4-241-115-14"] = "Kr-6"
	cards["136-4-134-149-159"] = "Kr-7"
	cards["136-4-52-140-52"] = "Kr-8"
	cards["136-4-117-115-138"] = "Kr-9"
	cards["136-4-115-146-109"] = "Kr-10"
	cards["136-4-61-140-61"] = "Kr-B"
	cards["136-4-48-107-215"] = "Kr-D"
	cards["136-4-108-155-123"] = "Kr-K"
	cards["136-4-94-164-118"] = "Kr-A"

	def getCardFromUID(self, uid):
		try:
			return self.cards[uid]
		except KeyError:
			return None
