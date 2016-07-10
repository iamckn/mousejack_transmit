This is code extending the mousejack tools https://github.com/RFStorm/mousejack.  
Replay/transmit tools have been added to the original tools.  
POC packets based on a **Logitech Wireless Combo MK220 which consists of a K220 wireless keyboard and an M150 wireless mouse** are included in the logs folder.  
More details available here https://www.ckn.io/blog/2016/07/09/hijacking-wireless-mice-and-keyboards/

#Usage

## scanner

Pseudo-promiscuous mode device discovery tool, which sweeps a list of channels and prints out decoded Enhanced Shockburst packets. 

```
usage: ./nrf24-scanner.py [-h] [-c N [N ...]] [-v] [-l] [-p PREFIX] [-d DWELL]

optional arguments:
  -h, --help                          show this help message and exit
  -c N [N ...], --channels N [N ...]  RF channels
  -v, --verbose                       Enable verbose output
  -l, --lna                           Enable the LNA (for CrazyRadio PA dongles)
  -p PREFIX, --prefix PREFIX          Promiscuous mode address prefix
  -d DWELL, --dwell DWELL             Dwell time per channel, in milliseconds
```

Scan for devices on channels 1-5

```
./nrf24-scanner.py -c {1..5}
```

Scan for devices with an address starting in 0xA9 on all channels

```
./nrf24-scanner.py -p A9
```


## sniffer

Device following sniffer, which follows a specific nRF24 device as it hops, and prints out decoded Enhanced Shockburst packets from the device. 
This version has also been modified to log the packets to a log file

```
usage: ./nrf24-sniffer.py [-h] [-c N [N ...]] [-v] [-l] -a ADDRESS -o OUTPUT [-t TIMEOUT] [-k ACK_TIMEOUT] [-r RETRIES] 

optional arguments:
  -h, --help                                 show this help message and exit
  -c N [N ...], --channels N [N ...]         RF channels
  -v, --verbose                              Enable verbose output
  -l, --lna                                  Enable the LNA (for CrazyRadio PA dongles)
  -a ADDRESS, --address ADDRESS              Address to sniff, following as it changes channels
  -o OUTPUT, --output OUTPUT                 Output file to log the packets
  -t TIMEOUT, --timeout TIMEOUT              Channel timeout, in milliseconds
  -k ACK_TIMEOUT, --ack_timeout ACK_TIMEOUT  ACK timeout in microseconds, accepts [250,4000], step 250
  -r RETRIES, --retries RETRIES              Auto retry limit, accepts [0,15]
```

Sniff packets from address 8C:D3:0F:3E:B4 on all channels and save them to output.log

```
./nrf24-sniffer.py -a 8C:D3:0F:3E:B4 -o logs/output.log
```

## replay/transmit

Replay captured packets or transmit generated ones. It follows a specific nRF24 device as it hops, and sends packets from a log file.

```
usage: ./nrf24-replay.py [-h] [-c N [N ...]] [-v] [-l] -a ADDRESS -i INPUT_FILE [-t TIMEOUT] [-k ACK_TIMEOUT] [-r RETRIES] 

optional arguments:
  -h, --help                                 show this help message and exit
  -c N [N ...], --channels N [N ...]         RF channels
  -v, --verbose                              Enable verbose output
  -l, --lna                                  Enable the LNA (for CrazyRadio PA dongles)
  -a ADDRESS, --address ADDRESS              Address to sniff, following as it changes channels
  -o INPUT_FILE, --input INPUT_FILE          Input file that has the packets to sned
  -t TIMEOUT, --timeout TIMEOUT              Channel timeout, in milliseconds
  -k ACK_TIMEOUT, --ack_timeout ACK_TIMEOUT  ACK timeout in microseconds, accepts [250,4000], step 250
  -r RETRIES, --retries RETRIES              Auto retry limit, accepts [0,15]
```

Send packets from file keystroke.log to address 8C:D3:0F:3E:B4 on hopping channel 

```
./nrf24-replay.py -a 8C:D3:0F:3E:B4 -i logs/keystroke.log
```

## network mapper

Star network mapper, which attempts to discover the active addresses in a star network by changing the last byte in the given address, and pinging each of 256 possible addresses on each channel in the channel list. 

```
usage: ./nrf24-network-mapper.py [-h] [-c N [N ...]] [-v] [-l] -a ADDRESS [-p PASSES] [-k ACK_TIMEOUT] [-r RETRIES]

optional arguments:
  -h, --help                                 show this help message and exit
  -c N [N ...], --channels N [N ...]         RF channels
  -v, --verbose                              Enable verbose output
  -l, --lna                                  Enable the LNA (for CrazyRadio PA dongles)
  -a ADDRESS, --address ADDRESS              Known address
  -p PASSES, --passes PASSES                 Number of passes (default 2)
  -k ACK_TIMEOUT, --ack_timeout ACK_TIMEOUT  ACK timeout in microseconds, accepts [250,4000], step 250
  -r RETRIES, --retries RETRIES              Auto retry limit, accepts [0,15]
```

Map the star network that address 61:49:66:82:03 belongs to

```
./nrf24-network-mapper.py -a 61:49:66:82:03
```

## continuous tone test

The nRF24LU1+ chips include a test mechanism to transmit a continuous tone, the frequency of which can be verified if you have access to an SDR. There is the potential for frequency offsets between devices to cause unexpected behavior. For instance, one of the SparkFun breakout boards that was tested had a frequency offset of ~300kHz, which caused it to receive packets on two adjacent channels.

This script will cause the transceiver to transmit a tone on the first channel that is passed in. 

```
usage: ./nrf24-continuous-tone-test.py [-h] [-c N [N ...]] [-v] [-l]

optional arguments:
  -h, --help                          show this help message and exit
  -c N [N ...], --channels N [N ...]  RF channels
  -v, --verbose                       Enable verbose output
  -l, --lna                           Enable the LNA (for CrazyRadio PA dongles)

```

Transmit a continuous tone at 2405MHz

```
./nrf24-continuous-tone-test.py -c 5
```

## Packet generator script

This uses a dictionary to map keyboard presses to the equivalent packets. It reads stdin input and logs the mapped packets to logs/keystrokes.log.
It will accept input until Ctrl+C is pressed.

```
usage: ./keymapper.py 
```

# Log files

The folder **logs** contains various pre-saved packets for various keyboard operations.  
**Shell.log** is for exploitation of a Windows machine by running a powershell one-liner which connects back to the attacker machine.  

The file **keys.log** serves as a reference where various key presses and combinations are mapped to their equivalent packets.

# Demo

A demo of exploiting a Windows machine can be found here https://www.youtube.com/watch?v=YLzUeK1IvJs&feature=youtu.be
