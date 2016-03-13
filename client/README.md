# jawsfi client

This directory contains the source code that is used by clients of the jawsfi project. Clients refer to the Raspberry Pi B+ that run the application. 

The Pi's are currently specced as follows:
1 x Raspberry Pi B+ running Rasbian OS
1 x Pi WiFi USB Adapter
1 x TP-LINK WiFi USB Adapter (capable of advanced monitoring features)
1 x Power Adapter

Dependencies

- Python 2.7
- pyshark library (https://github.com/KimiNewt/pyshark)

## Registering a device
```
$ ./jawsfi.py register -n <name>
```

## Sniffing traffic
```
$ sudo ./jawsfi.py sniff -i <interface>
```