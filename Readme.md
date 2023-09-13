## python_server
Server software to forward commands from controllers (`desktop_client` and `webclient`)
to lighting fixtures (`dmx_receiver` and `strobo_receiver`).

## desktop_client
Desktop client written in Python and Qt to generate the commands for controlling a DMX fixture and stroboscope.

## webclient
Web-based client written in Javascript to generate the commands for controlling a DMX fixture and stroboscope.

## dmx_receiver
Arduino software that listens for DMX commands on a TCP socket and outputs these as DMX signals on the serial port.
Also includes support for a relay output to turn on/off power to the controlled device.

## strobo_receiver
Software for ESP8266. It listens for commands on a TCP socket to turn on/off an output pin. A lamp can be connected
to the output to create a stroboscope.

## Hardware support
- A complete stroboscope can be built using an ESP8266 module (NodeMCU), a power mosfet (IRLZ44N), and a LED light
source with a discrete DC power supply.
- The DMX receiver can be built using an Arduino (Uno or Leonardo) and a DMX shield. Add an AC solid state relay for
controlling power to the controlled device.
- The clients support generating DMX commands for the ADJ Fog Fury Jett DMX controlled smoke machine.
