import requests
import json
import urllib2
import subprocess
import codecs
import datetime
import re
from datetime import date

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

newsurl = 'https://newsapi.org/v2/top-headlines?sources=cnn&apiKey=fd1f73ccf65745eabbf8ec2d8aa0934e'
newsdata = json.load(urllib2.urlopen(newsurl))
articles = newsdata['articles']

article1Title = articles[0]['title']
article1Desc = articles[0]['description']

article2Title = articles[1]['title']
article2Desc = articles[1]['description']

article3Title = articles[2]['title']
article3Desc = articles[2]['description']

article4Title = articles[3]['title']
article4Desc = articles[3]['description']
newsText = "Today in the news.\r\n";
for x in range(0, 3):
    if(articles[x]['title'] is not None and articles[x]['description'] is not None):
        newsText += articles[x]['title']+"... "+articles[x]['description']+"\r\n..."

timeOfDay = "Good morning Jaskarn"
now = datetime.datetime.now()
hour = now.hour
sunriseMinutes = (sunrise.split(':')[1]).split(' ')[0]
sunsetMinutes = (sunset.split(':')[1]).split(' ')[0]
if(int(sunriseMinutes) <= 9):
    sunrise = str(sunrise.split(':')[0])+":0"+sunriseMinutes
if(int(sunsetMinutes) <=9):
    sunset = str(sunset.split(':')[0])+":0"+sunsetMinutes
print(sunrise)
if(hour >11 and hour < 16):
   timeOfDay = "Good afternoon Jaskarn"
elif (hour >= 16):
   timeOfDay = "Good evening Jaskarn"

minutes = str(now.minute)
if(int(minutes) <= 9):
 minutes = "0"+minutes
if(hour <= 9):
    hour = "0"+hour
if(hour > 12):
    hour = hour-12
    minutes=minutes+" p.m."
else:
    minutes=minutes+" a.m."
time = str(hour)+":"+minutes

result =  str(date(2018, 4, 12) - date.today())
daysleft = int(result.split(' ')[0])
if(daysleft <= 9):
    daysleft = "0"+str(daysleft)
if(daysleft == 1):
    resultString = str(daysleft)+" day"
else:
    resultString = str(daysleft)+" days"
pollyText = timeOfDay+", it is "+time+". Today in "+str(location)+", California, the weather will be "+str(currentCondition)+". Currently it is "+str(currentTemp)+" with an expected low of "+str(lowTemperature)+" and a high of "+str(highTemperature)+". Sunrise is expected to occur at "+sunrise+" and sunset will occur at "+sunset+".\r\n"+newsText+" Keep it up, "+resultString+" left!"
#print(pollyText)
text_file = open("weather.txt", "w")
text_file.write(pollyText.encode('utf-8'))
text_file.close()
f = codecs.open("weather.txt", encoding='utf-8')

cnt = 0
file_names = ''

for line in f:
    rendered = ''
    line = line.replace('"', '\\"')
    command = '~/.local/bin/aws polly synthesize-speech --text-type ssml --output-format "mp3" --voice-id "Brian" --text "{0}" {1}'

    if '\r\n' == line:
        #A pause after a paragraph
        rendered = '<speak><break time= "2s"/></speak>'
    else:
        #A pause after a sentence
        rendered = '<speak><amazon:effect name=\\"drc\\">' + line.strip() + '<break time=\\"1s\\"/></amazon:effect></speak>'
    
    file_name = ' polly_out{0}.mp3'.format(u''.join(str(cnt)).encode('utf-8'))
    cnt += 1
    command = command.format(rendered.encode('utf-8'), file_name)
    file_names += file_name
    print command
    subprocess.call(command, shell=True)

print file_names
execute_command = 'cat ' + file_names + '>result.mp3'
subprocess.call(execute_command, shell=True)

execute_command = 'rm ' + file_names
print 'Removing temporary files: ' + execute_command

subprocess.call(execute_command, shell=True)
subprocess.call("/home/pi/scripts/hdmi-on.sh", shell=True)
subprocess.call("mpg321 /home/pi/alarm.mp3", shell=True)
subprocess.call("mpg321 result.mp3", shell=True)
