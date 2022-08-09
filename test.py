import re
import threading
from flask import Flask
from flask import render_template
import time
from datetime import datetime as dt
import adafruit_dht
#from board import D18
import csv
from flask.json import jsonify
import bme280
import smbus2
import random as rd


app = Flask(__name__)

port = 1
address = 0x76

@app.route('/json')
def serve_homepage():
    
    return render_template('main.html')

@app.route('/api')
def apipoint():
    data = {
        'tmp' : rd.randint(12, 43),
        'hum' : rd.randint(45, 92),
        'press' : rd.randint(880, 1143),
        'time' : dt.fromtimestamp(time.time())
    }


    with open('./static/infos.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data.get('time'), data.get('tmp'), data.get('hum'), data.get('press')))
    return jsonify(data)

@app.route('/')
def jsonr():
	return render_template('json.html')


if __name__ == '__main__':
	#t1 = threading.Thread(target= show_lcd)
	#t1.start()
	#t1.join()

	app.run(host= '127.0.0.1', debug= True, port= 8000)
