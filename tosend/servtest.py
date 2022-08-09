
# Importation des modules necessaires
from flask import Flask # Objet application Flask du module Flask
from flask import render_template # Fonction de rendu des pages html du modue Flask
from datetime import datetime as dt # Classe datetime pour l'obtention du timestamp
import adafruit_dht # Module pour la connexion au capteur DHT22
from board import D18 # Module pour la gestion des ports
import csv # Module pour la gestion du fichier csv
from flask.json import jsonify # Fonction du module Flask pour la mise au format JSON des données
import bme280 # Module pour la connexion au capteur bme280
import smbus2 # Module de gestion des bus pour la connexion des capteurs


app = Flask(__name__) # Déclaration de l'application Flask pour le serveur

port = 1 # Définition du port pour la connexion au bme280
address = 0x76 # Définition de l'adresse pour la connexion au bme280

@app.route('/api') # Endpoint pour l'api, obtention des informations au format json
def apipoint(): # Déclaration de la fonction
	try:
		bus = smbus2.SMBus(port)

		calibration_params = bme280.load_calibration_params(bus, address)

		data_bus = bme280.sample(bus, address, calibration_params) # Connexion au bme280
		dht_device= adafruit_dht.DHT22(D18,use_pulseio=False) # Connexion au DHT22

		# Obtention des informations des capteurs
		temperature= str(dht_device.temperature) # Température
		humidity= str(dht_device.humidity) # Humidité
		pressure = data_bus.pressure # Pression
		
		# Affichage de la température et de l'humidité
		print(temperature,"°") 
		print(humidity,"°")

	except RuntimeError as e: # Si une RuntimeError est levée
		dht_device.exit() # Déconnecter le DHT22
		print("Runtime : ", e.args[0]) # Afficher l'erreur
		time_ = dt.now().strftime('%Y-%m-%d %H:%M:%S') # Obtenir le timestamp
		# Mettre None comme valeur par défaut et mettre les données sous format JSON
		data = {
		'error' : True,
		'tmp' : None,
		'hum' : None,
		'press' : None,
		'time' : time_
		}
	except Exception as e: # Si une autre classe d'erreur est levée
		# Gérer de la même manière que RuntimeError
		print(f'{e.__class__.__name__} : {e}')
		time_ = dt.now().strftime('%Y-%m-%d %H:%M:%S')
		data = {
		'error' : True,
		'tmp' : None,
		'hum' : None,
		'press' : None,
		'time' : time_
		}
	else: # Si la lecture des données se passe bien
		time_ = dt.now().strftime('%Y-%m-%d %H:%M:%S') # Obtenir le timestamp
		with open('./static/infos.csv', 'a') as f: # Ouvrir le fichier .csv en mode ajout
			writer = csv.writer(f) # Passer l'objet à un writer csv, pour l'écriture des données csv
			writer.writerow((time_  ,   temperature   ,    humidity    ,     pressure)) # Écriture des données dans le fichier .csv
		
		# Mettre les données sous forme de dict
		data = {
		'error' : False,
		'tmp' : temperature,
		'hum' : humidity,
		'press' : round(pressure, 3),
		'time' : time_
		}
	return jsonify(data) # Retourner les valeurs obtenues au format json

@app.route('/')
def jsonr(): # Définition de la fonction pour l'affichage de la page web
	return render_template('json.html') # Rendre le template à templates/json.html sur l'url /

if __name__ == '__main__': # Si le fichier servtest.py est éxecuté
	app.run(host= '10.1.1.117', debug= True, port= 8000) # Démarrer le serveur web
