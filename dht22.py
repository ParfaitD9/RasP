import adafruit_dht
from board import D18

dht_device=adafruit_dht.DHT22(D18)
temperature=dht_device.temperature
humidity= dht_device.humidity
print (temperature,"°")
print (humidity,"°")
