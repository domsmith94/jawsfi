import pyshark

'''
File used for testing out functions
'''

capture = pyshark.LiveCapture(interface='wlan0', display_filter='wlan.fc.type_subtype eq 4')
#capture.set_debug()

print 'Capturing all probe requests...'
for packet in capture.sniff_continuously(packet_count=50):
    print 'Device: ', packet.wlan.ta_resolved, ' Signal: ', packet.radiotap.dbm_antsignal ,'db'
