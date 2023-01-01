from machine import Pin
import dht
import time
import network
import urequests
from os import getenv, putenv

ssid = os.getenv('WIFI_SSID')
password = os.getenv('WIFI_PASSWORD')
location = os.getenv('LOCATION')
influxurl = os.getenv('INFLUX_URL')

wlan = network.WLAN(network.STA_IF)
wlan.active(True),
wlan.connect(ssid, password)
 
# Wait for connect or fail
max_wait = 300
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

#Connected to WIFI :)

d = dht.DHT22(machine.Pin(28))
while True:
    time.sleep(10)
    
    try:
        d.measure()
    except:
        print("An exception occurred reading from the dht22")
        
    t = d.temperature()
    h=d.humidity()
    print("Temp: {}c".format(t))
    print("Humidity: {}%".format(h))
    
    
    data = "temperature,room={} temperature={},humidity={}".format(location,t,h)
    try:
        r = urequests.post(influxurl,data=data)
    except:
        print("An exception occurred")
    finally:
        r.close()
    #print(r.json())
    
    
    

