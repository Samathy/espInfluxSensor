import argparse
import os
import pathlib

from ampy.pyboard import Pyboard
from ampy.files import Files

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
SSID = os.environ["SSID"] 
PASS = os.environ["PASS"]
DBNAME = os.environ["DBNAME"]
INFLUXUSR = os.environ["INFLUXUSR"]
INFLUXPASSWD = os.environ["INFLUXPASSWD"]
METRICNAME = os.environ["METRICNAME"]

parser = argparse.ArgumentParser()
parser.add_argument("-l", help="Location of sensor", required=True, action="store", type=str)
parser.add_argument("-f", help="Flash main.py and settings.py to ESP", required=False, action="store_true")
parser.add_argument("-s", help="Serial Port", type=str, default="/dev/tty/USB0", required=False)
parser.add_argument("-b", help="Baud rate", type=str, default=str(115200), required=False)
parser.add_argument("-p", help="DS Sensor data pin number", type=int, default=4, required=False)
parser.add_argument("-i", help="Interval between data gathering ( seconds )", type=int, default=10, required=False)

args = parser.parse_args()

settings_file = (
        f"HOST = '{HOST}'\n"
        f"PORT = {PORT}\n"
        f"SSID = '{SSID}'\n"
        f"PASS = '{PASS}'\n"
        f"LOCATION = '{args.l}'\n"
        f"METRICNAME = '{METRICNAME}'\n"
        f"DBNAME =  '{DBNAME}'\n"
        f"INFLUXUSR = '{INFLUXUSR}'\n"
        f"INFLUXPASSWD = '{INFLUXPASSWD}'\n"
        f"DSPIN = {args.p}\n"
        f"INTERVAL = {args.i}\n")

with open("src/settings.py", "w") as settings:
    settings.write(settings_file)

print("Wrote settings file")

if args.f:
    print("Flashing new firmware...")

    pyboard = Pyboard(args.s, baudrate=args.b)
    files = Files(pyboard)
    for f in [pathlib.Path("src/main.py"), pathlib.Path("src/settings.py")]:
        with open(f, "r") as infile:
            files.put(f.name, infile.read())

    print("Completed flashing")


