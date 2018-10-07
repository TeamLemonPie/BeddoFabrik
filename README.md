## BeddoFabrik

BeddoFabrik is a tool in the "Beddo" product family. The products are designed to create an overlay for a poker live stream.
It's main purpose is to manage up to five NFC scanners that are connected to a Rasperry Pi Zero W and send information about detected cards to BeddoMischer.

![](/build/resources/icon_112x112.png) (Icon made by <a href="https://www.flaticon.com/authors/vectors-market" title="Vectors Market">Vectors Market</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>)

### Main Features
- can be used on any Rasperry Pi
- allows to connect up to five NFC scanners (RC522 modules are used)
- detect cards from the scanners
- validate if the scanned cards already has been scanned (This is accomplished by storing already detected cards in an internal list for every connected scanner.)
- send information about scanned cards to BeddoMischer
- listen for clear commands (If a clear command is received the internal list of already scanned cards for a certain scanner will be cleared. This is used to initiate a new round.)
- detect manage cards (A manage card can be used to assign a new seat to a player. This is accomplished by placing the manage card for a player on a certain NFC reader at the table. The seat is then automatically assigned to the player the manage card corresponds to.)
- automatic discover of BeddoMischer ip address by sending requests to the network- 


![](/build/resources/BeddoFabrik_wiring.png)
![](/build/resources/raspberry-pi-pinout-5-readers.png)


### Mounting the NFC scanners
The NFC scanners need to be mounted underneath the poker table. To avoid any physical harm to the circuit boards the scanners are embedded in a wood structure that is mounted to the table.

![](/build/resources/scanner_mount_single_1.png)
![](/build/resources/scanner_mount_single_2.png)

To increase the flexibility all scanners will be equipped with RJ45 jacks. This allows the usage of normal ethernet wires to connect the scanners with the Rasperry Pis.
Our particular setup includes seven player scanners and five board scanners. That's the reason why we used three Raspberry Pis. All of the twelve ethernet wires will arrive in an ethernet patch panel. Originating form this patch panel the individual wires of every ethernet cable are connected to the GPIO pins of the raspberry pis.

![](/build/resources/patch_panel.JPG)
![](/build/resources/complete_table.JPG)

### Used Libraries
![SPI-Py](https://github.com/lthiery/SPI-Py)