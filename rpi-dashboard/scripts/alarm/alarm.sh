#!/bin/bash
#crontab -u pi -l | grep -v 'mpg321 /home/pi/alarm.mp3'  | crontab -u pi -
#(crontab -u pi -l ; echo "45 6 * * * mpg321 /home/pi/alarm.mp3") | crontab -u pi -
echo "$1 $2 * * * python /home/pi/scripts/alarm/getWeather.py" > /home/pi/scripts/alarm/alarmjob.txt
crontab /home/pi/scripts/alarm/alarmjob.txt
