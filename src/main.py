import socket
import network
import machine, onewire, ds18x20, time

import settings

class DSInfo:
    def __init__(self):
        print("Setting up DS sensor")
        self.ds_pin = machine.Pin(settings.DSPIN)
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(self.ds_pin))

        self.roms = self.ds_sensor.scan()
        print("roms:")
        print(self.roms)

    def get_temperature(self):
        if self.roms:
            self.ds_sensor.convert_temp()
            return self.ds_sensor.read_temp(self.roms[0]) # We're only going to have one sensor per-board
        else:
            return 0


def wifi_setup():
    print("Setting up WiFi")
    interface = network.WLAN(network.STA_IF)
    if not interface.isconnected():
        print("No interface connected")
        interface.active(True)
        interface.connect(settings.SSID, settings.PASS)
        time.sleep(4)
        if not interface.isconnected():
            print("Unable to connect to WiFi "+ str(interface.status()))
        print("WiFi connected to "+settings.SSID)

    return interface
        

def http_post(host, port, path, auth_token, data):
    print("Sending http request")
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    print("Sending bytes...:"+str(s.send(bytes('POST /%s HTTP/1.1\r\nHost: /%s\r\nAuthorization: Token /%s\r\nContent-Length: /%s\r\nContent Type: application/x-www-form-urlencoded\r\n\r\n /%s'.format(path, host+":"+port, auth_token, str(len(data)), data)))))
    print("Waiting to receive bytes")
    while True:
        recieved = s.recv(100)
        if recieved:
            print(str(recieved, 'utf8'), end='')
        else:
            break
    s.close()

def deep_sleep(seconds):
    print("Sleeping for 10")
    time.sleep(10)

interface = wifi_setup()
sensors = DSInfo()

while True:
    http_post(settings.HOST, settings.PORT, "/api/v2/write/?bucket=/%s&precision=s".format(settings.DBNAME), settings.INFLUXUSR+":"+settings.INFLUXPASSWD, "/%s, location=/%s, value=/%s".format(settings.METRICNAME, settings.LOCATION, sensors.get_temperature()))
    deep_sleep(10)
