import serial
import sys
import math

if len(sys.argv) != 2:
	print("Usage example : python3 compass.py /dev/ttyACM1")
	exit(1)


def compute_heading(x, y, z, declination_angle=-0.01745329, in_degree=False):
	angle = math.atan2(y, x)
	angle += declination_angle
	if angle < 0:
		angle += 2*math.pi
	elif angle > 2*math.pi:
		angle -= 2*math.pi
	if in_degree:
		angle = angle * 180/math.pi
	return angle

serial_port = sys.argv[1]

serial_compass = serial.Serial(serial_port, timeout=1)

while 1:
	raw_measurement = serial_compass.readline()

	# Decode binary measurement
	measurements = raw_measurement.decode("utf8")
	# Remove final \n
	measurements = measurements[:-1]
	# Split along tabs
	measurements = measurements.split("\t")
	# Parse measurements
	try:
		measurements = list(map(lambda val: float(val), measurements))
	except:
		continue

	heading = round(compute_heading(measurements[0], measurements[1], measurements[2], in_degree=True)*100)/100

	print("X: {} µT,\tY: {} µT,\tZ: {} µT,\t{}°".format(measurements[0], measurements[1], measurements[2],heading))