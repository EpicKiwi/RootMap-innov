import sys
import time

import serial

if len(sys.argv) != 2:
	print("Usage example : python3 pyserial.py /dev/ttyACM1")
	exit(1)

serial_compass = serial.Serial(sys.argv[1], timeout=1)


try:

	while 1:

		try:
			input = serial_compass.readline().decode("utf8")[:-1]
		except UnicodeEncodeError:
			continue

		print("{}\t{}".format(time.time(), input), flush=True)

except KeyboardInterrupt:
	exit(0)