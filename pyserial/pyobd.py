import sys
import time

import obd

if len(sys.argv) != 2:
	print("Usage example : python3 pyobd.py /dev/ttyACM1")
	exit(1)

connection = obd.OBD(portstr=sys.argv[1])

try:

	while 1:

		speed = connection.query(obd.commands.SPEED).value
		speed_m_s = speed.magnitude / 3.6

		print("{}\t{}".format(time.time(), speed), flush=True)

except KeyboardInterrupt:
	exit(0)