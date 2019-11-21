import time

import serial
import sys
import math
import obd

if len(sys.argv) != 2:
	print("Usage example : python3 compass.py /dev/ttyACM1")
	exit(1)


def get_time():
	return time.time()


def get_speed():
	if connection.status() == obd.OBDStatus.CAR_CONNECTED :
		speed = connection.query(obd.commands.SPEED).value
		return speed.magnitude / 3.6
	else:
		return 8

def compute_heading(x, y, z, declination_angle=-0.01745329, in_degree=False):
	angle = math.atan2(y, x)
	angle += declination_angle
	if angle < 0:
		angle += 2*math.pi
	if angle > 2*math.pi:
		angle -= 2*math.pi
	if in_degree:
		angle = angle * 180/math.pi
	return angle

# obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.OBD()

if connection.status() != obd.OBDStatus.CAR_CONNECTED:
	print("ODB Adapter not connected, using constant speed of 8 m/s", file=sys.stderr)

serial_port = sys.argv[1]
serial_compass = serial.Serial(serial_port, timeout=1)
last_pos = (0, 0)
last_point_time = get_time()
full_distance = 0
time_elapsed = 0
slowmode = False
next_write = 0

try:

	while 1:
		raw_measurement = serial_compass.readline()

		# Decode binary measurement
		try :
			measurements = raw_measurement.decode("utf8")
		except UnicodeDecodeError:
			continue
		# Remove final \n
		measurements = measurements[:-1]
		# Split along tabs
		measurements = measurements.split("\t")
		# Parse measurements

		if len(measurements) < 3:
			continue

		try:
			measurements = list(map(lambda val: float(val), measurements))
		except:
			continue

		heading = compute_heading(measurements[0], measurements[1], measurements[2])

		speed = get_speed()

		current_time = get_time()

		deltatime = (current_time - last_point_time)

		distance = speed * deltatime

		current_pos = (
			last_pos[0] + distance * math.sin(heading),
			last_pos[1] + distance * math.cos(heading)
		)


		full_distance += distance
		time_elapsed += deltatime
		last_pos = current_pos
		last_point_time = current_time

		if slowmode == True and next_write < time_elapsed:
			print("{};{};{}".format(
				current_pos[0],
				current_pos[1],
				speed), flush=True)
			next_write = time_elapsed + 0.05

		serial_compass.flushInput()

except KeyboardInterrupt:
	exit(0)