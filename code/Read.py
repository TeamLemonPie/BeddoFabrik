#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import json
from Sender import Sender
from Cards import Cards
from Settings import Settings

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

settings = Settings()
readers = settings.getReaders()

print("{} devices registered:".format(len(readers)))
for x in readers:
    print(x)

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
                # if this method returns true then send new card to BeddoMischer

                isNewCard = currentReader.isNewCard(uid)
                # TODO: remove debug print
                print(isNewCard)
                if isNewCard:
                    card = Cards()
                    card = card.getCardFromUID(uid)
                    if card is not None:
                        dataDict = {
                            "scope": "reader",
                            "command": "card",
                            "key": currentReader.id,
                            "value": card
                        }

                        data = json.dumps(dataDict)

                        sender = Sender("192.168.1.43", 9999, data)
                        if not sender.send():
                            currentReader.clearCardFromHold(uid)
        time.sleep(0.2)
