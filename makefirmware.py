import argparse
import os
import pathlib

from ampy.pyboard import Pyboard
from ampy.files import Files

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]

SSID = os.environ["SSID"] 
PASS = os.environ["PASSWORD"]

parser = argparse.ArgumentParser()
parser.add_argument("-l", help="Location of sensor", required=True, action="store", type=str)
parser.add_argument("-m", help="InfluxDB Metric Name", required=True, type=str, action="store")
parser.add_argument("-d", help="InfluxDB DB Name", required=True, type=str, action="store")
parser.add_argument("-f", help="Flash main.py and settings.py to ESP", required=False, action="store_true")
parser.add_argument("-s", help="Serial Port", type=str, default="/dev/tty/USB0", required=False)
parser.add_argument("-b", help="Baud rate", type=str, default=str(115200), required=False)

args = parser.parse_args()

settings_file = (
        f"HOST = '{HOST}'\n"
        f"PORT = '{PORT}'\n"
        f"SSID = '{SSID}'\n"
        f"PASS = '{PASS}'\n"
        f"LOCATION = '{args.l}'\n"
        f"METRICNAME = 'args.m'\n"
        f"DBNAME =  'args.d'\n")



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


