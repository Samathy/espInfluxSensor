import socket
from . import settings

def http_post(host, port, path, data):
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('POST /%s HTTP/1.1\r\nHost: /%s\r\nAuthorization: Token /%s\r\nContent-Length: /%s\r\nContent Type: application/x-www-form-urlencoded\r\n\r\n /%s'.format(path, host+":"+port, auth-token, str(len(data)), data)))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

def get_temperature():
    #dothings
    pass


while True:
    http_post(settings.HOST, settings.PORT, "/api/v2/write/?bucket=/%s&precision=s".format(settings.DBNAME), "/%s, location=/%s, value=/%s".format(settings.METRICNAME, settings.LOCATION, get_temperature()))
    #Deep Sleep
