# Raspberry Pi Relay Client
> Control a relay board with your Raspberry Pi over a LAN.

This is the command client for connecting to a [Rpirelayserver](https://github.com/mdtomo/rpirelayserver) instance running on your Raspberry Pi. Use this client to control your Raspberry Pi relay outputs. You can run this client directly on the Raspberry Pi or on any machine running on the same LAN as the Raspberry Pi. When the required relays have been switched on or off you can quit this client and the server will preserve the state of the relays.

## Installation/Usage
Rpirelayclient only has one external dependency - [Python Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)

`git clone https://github.com/mdtomo/rpirelayclient`
`cd rpirelayclient`

Change the settings in config.py to the ip and port of you Raspberry Pi. Change the labels of the relays as desired.

`pipenv install`
`pipenv shell`
`python rpirelayclient.py`

## Licence
This project is licensed under the MIT License - see the LICENSE.md file for details.
