import pyshark

capture = pyshark.LiveCapture(interface='en0')
capture.sniff(timeout=50)

for packet in capture.sniff_continuously(packet_count=5):
    print 'Just arrived:', packet