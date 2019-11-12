from time import sleep
import obd

obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.OBD(baudrate=9600)

if connection.status() != obd.OBDStatus.CAR_CONNECTED:
	print("Adapter not connected")
	exit(1)

while 1:
	speed_res = connection.query(obd.commands.SPEED)
	rpm_res = connection.query(obd.commands.RPM)
	temp_res = connection.query(obd.commands.OIL_TEMP)
	accel_pos = connection.query(obd.commands.RELATIVE_ACCEL_POS)

	print("{} %, {} rpm, {} Km/h, {}°C".format(accel_pos.value, rpm_res.value, speed_res.value, temp_res.value))

	sleep(0.1)
