"""Read temperature and humidity from dth11 sensor attached via arduino."""

import serial
import json
import traceback
from time import sleep
from datetime import datetime

DATAFILE = "./data/my_room.json"

# Find with
#
# $ ls /dev/tty.*
#
PORT = "/dev/tty.usbmodem1411"
BAUD = 9600


def process_line(line):
    """Extract data from Arduino output line and return as object."""
    rv = {
        "date": datetime.now().isoformat()
    }

    line = line.decode('utf-8')

    if line.find("FAIL") > 0:
        rv["state"] = "FAIL"
    else:
        rv["state"] = "OK"
        temp_pos = line.find("C")
        hum_pos = line.find("H")
        try:
            rv["temperature"] = float(line[temp_pos - 2:temp_pos])
            rv["humidity"] = float(line[hum_pos - 2:hum_pos])
        except ValueError:
            print("ValueError reading data from line:\n", line)
            traceback.print_exc()
            rv["state"] = "FAIL"
    return rv


def write_to_file(data):
    """Append JSON encoded data to file."""
    with open(DATAFILE, "a") as f:
        f.write(json.dumps(data))
        f.write("\n")


if __name__ == "__main__":
    ser = serial.Serial(PORT, BAUD)
    print(ser.name)

    while True:
        line = ser.readline()
        data = process_line(line)
        print(data)
        write_to_file(data)
        sleep(0.1)
