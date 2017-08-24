#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from Reader import Reader

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# List of readers
readers = []
readers.append(Reader(id=0, bus=0, subbus=0, reset=16))
readers.append(Reader(id=1, bus=1, subbus=1, reset=31))

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
                print(isNewCard)
                if isNewCard:
                    #TODO: send to BeddoMischer
                    pass
        time.sleep(0.2)
        print("round")

