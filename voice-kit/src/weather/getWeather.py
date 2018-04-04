import requests
import json
import urllib2
import subprocess
import codecs
import datetime

# open the url and the screen name 
# (The screen name is the screen name of the user for whom to return results for)
url = "http://api.wunderground.com/api/3bcfe92b211b3e4c/conditions/q/CA/Yuba_City.json"
# this takes a python object and dumps it to a string which is a JSON
# representation of that object
data = json.load(urllib2.urlopen(url))

# print the result
observation = data['current_observation']
city = observation['display_location']['full']
time = observation['local_time_rfc822']
weather = observation['weather']
currentTemp = observation['temp_f']
humidity = observation['relative_humidity']
wind = observation['wind_string']
percipitation = observation['precip_today_in']
now = datetime.datetime.now()
time = str(now.hour)+":"+str(now.minute)

pollyText = "Good morning, it is " + str(time) +". Today in "+city+" the weather is "+weather+", the current temperature is "+str(currentTemp)+". The wind chill is "+wind+". Have a wonderful day!"
print(pollyText)
text_file = open("weather.txt", "w")
text_file.write(pollyText)
text_file.close()

f = codecs.open("weather.txt", encoding='utf-8')

cnt = 0
file_names = ''

for line in f:
    rendered = ''
    line = line.replace('"', '\\"')
    command = 'aws polly synthesize-speech --text-type ssml --output-format "mp3" --voice-id "Brian" --text "{0}" {1}'

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
subprocess.call("mpg321 ./result.mp3", shell=True)