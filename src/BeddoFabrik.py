#!/usr/bin/env python
from subprocess import Popen, PIPE

import RPi.GPIO as GPIO
from sqlite3 import Connection

import MFRC522
import signal
import time
import json
from Cards import Cards
from ManageCards import ManageCards
from ServerDiscover import ServerDiscover
from Settings import Settings
from Connection import Connection
from thread import start_new_thread
from Logger import Logger

class BeddoFabrik:
	def __init__(self):
		self._continueReading = True
		self._settings = None
		self._readers = []
		self._beddoMischerIP = None
		self._connection = None

	def Start(self):
		# hook the SIGINT
		signal.signal(signal.SIGINT, self.__EndRead)

		# load settings
		self._settings = Settings()
		self._readers = self._readers
		Logger.debug("{} devices registered:".format(len(self._readers)))
		for x in self._readers:
			Logger.debug(x)

		# wait for wifi
		Logger.debug("Waiting for Wifi connection...")
		while not self.__IsWifiConnected():
			time.sleep(1)
		Logger.debug("Wifi connected")

		# discover BeddoMischer IP
		discoverer = ServerDiscover()
		self._beddoMischerIP = discoverer.Discover()

		# connect with server
		self.__Connect()

		# start thread to listen for incoming clear requests
		start_new_thread(self.__ListenForClearRequests, ())

		self.__MainLoop()

	# Capture SIGINT for cleanup when the script is aborted
	def __EndRead(self, signal, frame):
		Logger.info("Ctrl+C captured, ending read.")
		self._continueReading = False
		GPIO.cleanup()
		self._connection.active = False
		self._connection.close()

	def __IsWifiConnected(self):
		process = Popen(['iwconfig', 'wlan0'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = process.communicate(b"")
		returnCode = process.returncode
		if returnCode == 0 and "ESSID" in output:
			return True

		return False

	def __Connect(self):
		if self._connection is None or not self._connection.active:
			self._connection = Connection()
			self._connection.connect(self._beddoMischerIP, self._settings.server["port"])

	def __ListenForClearRequests(self):
		while True:
			try:
				requestData = self._connection.read()
				self.__HandleClearRequest(requestData.strip())
			except:
				self.__Connect()

	def __HandleClearRequest(self, requestData):
		if requestData == "":
			return

		requestData = requestData.split("\n")
		for line in requestData:
			try:
				obj = json.loads(line)
				key = obj["key"]
				Logger.debug("Received Clear: {}".format(key))
				if key == -1:
					self.__ClearAllHolds()
				else:
					self.__ClearHold(key)
			except:
				Logger.error("Error while parsing JSON. Data: {}".format(line))

	def __ClearAllHolds(self):
		for reader in self._readers:
			reader.clearHold()

	def __ClearHold(self, readerID):
		for reader in self._readers:
			if reader.id == readerID:
				reader.clearHold()

	def __MainLoop(self):
		while self._continueReading:
			for currentReader in self._readers:
				if not currentReader.activated:
					continue

				reader = MFRC522.MFRC522(bus=currentReader.bus,
										 subbus=currentReader.subbus,
										 reset=currentReader.reset)

				self.__HandleReader(reader, currentReader)

				reader.Close()
				time.sleep(0.2)


	def __HandleReader(self, reader, currentReader):
		(_, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
		(status, uid) = reader.MFRC522_Anticoll()

		if status != reader.MI_OK:
			return

		uid = "-".join(map(str, uid))

		# check if detected card is manage card
		if self.__HandleManageCard(uid, currentReader):
			return

		self.__HandleNormalCard(uid, currentReader)

	def __HandleManageCard(self, uid, currentReader):
		manageCards = ManageCards()
		manageCard = manageCards.getCardFromUID(uid)

		if manageCard is None:
			return False

		Logger.debug("Reader {} detected manage card: {}".format(currentReader.id, manageCard))

		dataDict = {
			"scope": "READER",
			"command": "manageCard",
			"key": currentReader.id,
			"value": manageCard
		}

		data = json.dumps(dataDict)
		data += "\r\n"
		if not self._connection.send(data):
			Logger.error("Error while sending manage card to server")
			self.__Connect()

		return True

	def __HandleNormalCard(self, uid, currentReader):
		if not currentReader.isNewCard(uid):
			Logger.debug("Skipping detected card for reader {}".format(currentReader.id))
			return

		cards = Cards()
		card = cards.getCardFromUID(uid)
		if card is None:
			return

		Logger.debug("Reader {} detected new card: {}".format(currentReader.id, card))

		dataDict = {
			"scope": "READER",
			"command": "card",
			"key": currentReader.id,
			"value": card
		}

		data = json.dumps(dataDict)
		data += "\r\n"
		if not self._connection.send(data):
			Logger.error("Error while sending new card to server")
			self.__Connect()
			# card could not be sent due to connection issues
			currentReader.clearCardFromHold(uid)
