from time import sleep
import obd

# obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.OBD(fast=False, check_voltage=False, timeout=1)

if connection.status() != obd.OBDStatus.CAR_CONNECTED:
	print("Adapter not connected")
	exit(1)

while 1:
	speed_res = connection.query(obd.commands.SPEED)
	rpm_res = connection.query(obd.commands.RPM)

	rpm = rpm_res.value
	speed = speed_res.value

	print("{}, {}".format(rpm, speed))
