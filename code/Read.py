#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal
from Reader import Reader

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# List of readers
readers = []
readers.append(Reader(0, '/dev/spidev0.0', 16))
readers.append(Reader(1, '/dev/spidev1.1', 31))

print("{} devices registered:".format(len(readers)))
for x in readers:
    print(x)

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    print("\n")

    for reader in readers:
        print("Reader #{} @ {}".format(reader.id, reader.bus))

        reader = MFRC522.MFRC522(dev=reader.bus, reset=reader.reset)

        # Scan for cards
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        # If a card is found
        if status == reader.MI_OK:
            print("Card detected")

        # Get the UID of the card
        (status,uid) = reader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == reader.MI_OK:

            # Print UID
            print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

            # Select the scanned tag
            reader.MFRC522_SelectTag(uid)

            # Authenticate
            status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status == reader.MI_OK:
                reader.MFRC522_Read(8)
                reader.MFRC522_StopCrypto1()
            else:
                print("Authentication error")

