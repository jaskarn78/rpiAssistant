import requests
import json
import urllib2
import subprocess
import codecs
import datetime

# open the url and the screen name 
# (The screen name is the screen name of the user for whom to return results for)
url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22yuba%20city%2C%20ca%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
# this takes a python object and dumps it to a string which is a JSON
# representation of that object
data = json.load(urllib2.urlopen(url))
results = data['query']['results']['channel']
location = results['location']['city']
distanceUnits = results['units']['distance']
speedUnits = results['units']['speed']
pressureUnits = results['units']['pressure']
tempUnits = results['units']['temperature']
windChill = results['wind']['chill'] +" "+tempUnits
windDirecttion = results['wind']['direction']
windSpeed = results['wind']['speed']+" "+speedUnits
humidity = results['atmosphere']['humidity']
sunrise = results['astronomy']['sunrise']
sunset = results['astronomy']['sunset']
currentDate = results['item']['condition']['date']
currentTemp = results['item']['condition']['temp']+" degrees farenheit"
currentCondition = results['item']['condition']['text']
lowTemperature = results['item']['forecast'][0]['low']
highTemperature = results['item']['forecast'][0]['high']

print("Good morning, it is "+str(currentDate)+". Today in "+str(location)+", Ca the weather will be "+str(currentCondition)+". Currently it is "+str(currentTemp)+" with a low of "+str(lowTemperature)+" and a high of "+str(highTemperature)+" Sunrise is expected to occur at "+str(sunrise)+" and sunset will occur at "+str(sunset)+" ... Have a great day!")


