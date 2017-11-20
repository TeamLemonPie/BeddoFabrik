#!/usr/bin/env python

import RPi.GPIO as GPIO
from sqlite3 import Connection

import MFRC522
import signal
import time
import json
from Cards import Cards
from ManageCards import ManageCards
from Settings import Settings
from Connection import Connection
from thread import start_new_thread

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    connection.active = False
    connection.close()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# load settings
settings = Settings()
readers = settings.getReaders()

print("{} devices registered:".format(len(readers)))
for x in readers:
    print(x)

connection = Connection()
connection.connect(settings.server["ip"], settings.server["port"])

def read():
    global connection
    while True:
        try:
            data = connection.read()

            data = data.strip()
            if data != "":
                try:
                    data = json.loads(data)
                    key = data["key"]
                    print("Received Clear: {}".format(key))
                    if key == -1:
                        for reader in readers:
                            reader.clearHold()
                    else:
                        for reader in readers:
                            if reader.id == key:
                                reader.clearHold()
                except:
                    print("Error while parsing JSON. Data: {}".format(data))
        except:
            if not connection.active:
                connection = Connection()
                connection.connect(settings.server["ip"], settings.server["port"])

start_new_thread(read, ())

while continue_reading:
    for currentReader in readers:
        if currentReader.activated:
            reader = MFRC522.MFRC522(bus=currentReader.bus,
                                     subbus=currentReader.subbus,
                                     reset=currentReader.reset)

            # Scan for cards
            (_, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

            # Get the UID of the card
            (status, uid) = reader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == reader.MI_OK:
                uid = "-".join(map(str, uid))

                # check if detected card is manage card
                manageCards = ManageCards()
                manageCard = manageCards.getCardFromUID(uid)
                if manageCard is not None:
                    print("Reader {} detected manage card: {}".format(currentReader.id, manageCard))
                    dataDict = {
                        "scope": "reader",
                        "command": "manageCard",
                        "key": currentReader.id,
                        "value": manageCard
                    }

                    data = json.dumps(dataDict)
                    data += "\r\n"
                    if not connection.send(data):
                        print("Error while sending manage card to server")
                        if not connection.active:
                            connection = Connection()
                            connection.connect(settings.server["ip"], settings.server["port"])
                elif currentReader.isNewCard(uid):
                    cards = Cards()
                    card = cards.getCardFromUID(uid)
                    print("Reader {} detected new card: {}".format(currentReader.id, card))
                    if card is not None:
                        dataDict = {
                            "scope": "reader",
                            "command": "card",
                            "key": currentReader.id,
                            "value": card
                        }

                        data = json.dumps(dataDict)
                        data += "\r\n"
                        if not connection.send(data):
                            print("Error while sending new card to server")
                            if not connection.active:
                                connection = Connection()
                                connection.connect(settings.server["ip"], settings.server["port"])
                            # card could not be sent due to connection issues
                            currentReader.clearCardFromHold(uid)
                else:
                    print("Skipping detected card for reader {}".format(currentReader.id))
        time.sleep(0.2)
