import pyshark

capture = pyshark.LiveCapture(interface='wlan0', display_filter='wlan.fc.type_subtype eq 4')
capture.set_debug()
capture.sniff(timeout=5)

for packet in capture.sniff_continuously(packet_count=5):
    print 'Just arrived:', packet
