import threading
from flask import Flask
from flask import render_template
import time
from datetime import datetime as dt
import adafruit_dht
from board import D18
import csv
from flask.json import jsonify
import bme280
import smbus2


app = Flask(__name__)

port = 1
address = 0x76

@app.route('/json')
def serve_homepage():
	try:
		bus = smbus2.SMBus(port)

		calibration_params = bme280.load_calibration_params(bus, address)

		data_bus = bme280.sample(bus, address, calibration_params)
		dht_device= adafruit_dht.DHT22(D18, use_pulseio= False)

		temperature=  dht_device.temperature
		humidity= dht_device.humidity
		pressure= data_bus.pressure

		print(temperature,"°")
		print(humidity,"°")
	except RuntimeError as e:
		dht_device.exit()
		print("Runtime : ", e.args[0])
	except Exception as e:
		print(f'{e.__class__.__name__} : {e}')
	else:
		data = {
		'tmp' : temperature,
		'hum' : humidity,
		'press' : pressure,
		'time' : dt.fromtimestamp(time.time())
		}

		return render_template("main.html", **data, error= False)
	return render_template("main.html", error= True)

@app.route('/api')
def apipoint():
	try:
		bus = smbus2.SMBus(port)

		calibration_params = bme280.load_calibration_params(bus, address)

		data_bus = bme280.sample(bus, address, calibration_params)
		dht_device= adafruit_dht.DHT22(D18,use_pulseio=False)

		temperature= str(dht_device.temperature)
		humidity= str(dht_device.humidity)
		pressure = data_bus.pressure
		
		print(temperature,"°")
		print(humidity,"°")

	except RuntimeError as e:
		dht_device.exit()
		print("Runtime : ", e.args[0])
		time_ = dt.now().strftime('%Y-%m-%d %H:%M:%S')
		data = {
		'error' : True,
		'tmp' : None,
		'hum' : None,
		'press' : None,
		'time' : time_
		}
	except Exception as e:
		print(f'{e.__class__.__name__} : {e}')
		time_ = dt.now().strftime('%Y-%m-%d %H:%M:%S')
		data = {
		'error' : True,
		'tmp' : None,
		'hum' : None,
		'press' : None,
		'time' : time_
		}
	else:
		time_ = dt.now().strftime('%Y-%m-%d %H:%M:%S')
		with open('./static/infos.csv', 'a') as f:
			writer = csv.writer(f)

			writer.writerow((time_,   temperature,    humidity,     pressure))

		data = {
		'error' : False,
		'tmp' : temperature,
		'hum' : humidity,
		'press' : round(pressure, 3),
		'time' : time_
		}
	return jsonify(data)

@app.route('/')
def jsonr():
	return render_template('json.html')


def show_lcd():
	import I2C_LCD_driver
	mylcd = I2C_LCD_driver.lcd()
	

	while True:
		if int(time.time()) % 8 == 0:
			try:
				port = 1
				address = 0x76
				bus = smbus2.SMBus(port)


				calibration_params = bme280.load_calibration_params(bus, address)
				data = bme280.sample(bus, address, calibration_params)
				dht_device=adafruit_dht.DHT22(D18, use_pulseio= False)
	
				temperature=dht_device.temperature
				humidity= dht_device.humidity
				pressure = data.pressure
			except RuntimeError as e:
				print(e.args[0])
				dht_device.exit()
				time.sleep(2)
				continue
			except Exception as e:
				print(f'{e.__class__} : {e}')
				dht_device.exit()
			else:
				print (temperature,"°")
				print (humidity,"°")
				print (data.pressure)

				mylcd.lcd_display_string("Temp: %d %s C    " % (temperature, chr(223)), 1)
				mylcd.lcd_display_string("Humidity: %d %%" % humidity, 2)
				mylcd.lcd_display_string("Pressure: %d hpa "% pressure,3)
				dht_device.exit()

if __name__ == '__main__':
	t1 = threading.Thread(target= show_lcd)
	t1.start()
	#t1.join()

	app.run(host= '192.168.0.163', debug= True, port= 8000)
