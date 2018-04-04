#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

The Google Assistant Library can be installed with:
    env/bin/pip install google-assistant-library==0.0.2

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import subprocess
import sys
import aiy.assistant.auth_helpers
import aiy.audio
import aiy.voicehat
import time
import apa102
import threading
import pymysql
import datetime
from gpiozero import LED
try:
    import queue as Queue
except ImportError:
    import Queue as Queue
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from picamera import PiCamera
from time import sleep
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)
#connect to db
db = pymysql.connect("192.168.7.95", "jagpal78", "686Shanghai", "dashboard")
#setup cursor
cursor = db.cursor()
alarm = False
alarm_set = False
run = False
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")

def playError():
    subprocess.call("mpg321 /home/pi/sounds/problem.mp3", shell=True)
def speak(messagetospeak):
    pixels.speak()
    subprocess.call("/home/pi/scripts/say.sh "+messagetospeak, shell=True)
    pixels.wakeup()
def alarmTime():
    subprocess.call("/home/pi/scripts/setAlarm.sh", shell=True);
def power_off_pi():
    speak("'Good bye!'")
    subprocess.call('sudo shutdown now', shell=True)
def reboot_pi():
    speak("'See you in a bit!'")
    subprocess.call('sudo reboot', shell=True)
def play_song():
    try:
        subprocess.call("rsh pi@192.168.7.57 /home/pi/scripts/loadSongs.sh", shell=True)
    except:
        playError()
def loadPlaylist(playlist):
    print(playlist.encode('utf-8'))
def stop_song():
    try:
        print('stopping song')
        subprocess.call("rsh pi@192.168.7.57 mpc pause", shell=True)
    except:
        playError()
def next_song():
    try:
        print('next song')
        subprocess.call("rsh pi@192.168.7.57 mpc next", shell=True)
    except:
        playError()
def logRun(miles):
    print(""" INSERT INTO run(id, day, miles) values(0, %s,%s)""", (today, miles))
    try:
        cursor.execute(""" INSERT INTO run(id, day, miles) values(0, %s,%s)""", (today, miles))
        db.commit()
        subprocess.call("mpg321 /home/pi/sounds/runrecorded.mp3", shell=True)
    except:
        subprocess.call("mpg321 /home/pi/sounds/runfailed.mp3", shell=True)
        db.rollback()
def showRunningLog():
    try:
        cursor.execute(""" DELETE FROM ShowModal """)
        cursor.execute(""" INSERT INTO ShowModal values(%s)""", (1))
        db.commit()
        subprocess.call("mpg321 /home/pi/sounds/displaylog.mp3", shell=True)
    except:
        db.rollback()
def hideRunningLog():
    try:
        cursor.execute(""" DELETE FROM ShowModal """)
        cursor.execute(""" INSERT INTO ShowModal values(%s)""", (0))
        db.commit()
        subprocess.call("mpg321 /home/pi/sounds/closelog.mp3", shell=True)
    except:
        db.rollback()
def removeLastRun():
    try:
        cursor.execute(""" DELETE FROM run WHERE day = %s """, (today))
        cursor.execute(""" INSERT INTO ShowModal values(%s)""", (0))
        db.commit()
        subprocess.call("mpg321 /home/pi/sounds/deleterun.mp3", shell=True)
    except:
        db.rollback()
        subprocess.call("mpg321 /home/pi/sounds/deleterunfailed.mp3", shell=True)


def setAlarm(response):
    try:
        if(response == '' or response is None):
            assistant.stop_conversation()
            return
        else:
            morning = True
            if('p.m.' in response or 'a.m.' in response):
                morning = False
                alarm = response.split(' ')
                if('p.m.' in response):
                    hour = str(int(alarm[0].split(':')[0])+12)
                else: 
                    hour = alarm[0].split(':')[0]
                minutes = alarm[0].split(':')[1]
            elif('a.m.' in response):
                alarm = response.split(' ')
                hour = alarm[0].split(':')[0]
                minutes = alarm[1].split(':')[1]
            else:
                alarm = response.split(':')
                hour = alarm[0]
                minutes = alarm[1]
            if(morning == False):
                message = "Alarm set for "+str(int(hour)-12)+":"+minutes
            else: message = "Alarm set for "+hour+":"+minutes
            ssh(minutes, hour)
            subprocess.call("~/.local/bin/aws polly synthesize-speech --output-format mp3 --voice-id Brian --text '"+ str(message) +"' alarmset.mp3 && mpg321 alarmset.mp3", shell=True)
    except:
        playError()
def ssh(minutes, hour):
    subprocess.call("rsh pi@192.168.7.57 /home/pi/scripts/alarm/alarm.sh "+minutes+" "+hour, shell=True)

def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    global alarm
    global alarm_set
    global run
    if event.type == EventType.ON_START_FINISHED:
        pixels.wakeup()
        status_ui.status('ready')
        aiy.voicehat.get_status_ui().set_trigger_sound_wave('/home/pi/sounds/listening.wav')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        subprocess.call("aplay /home/pi/sounds/listening.wav", shell=True)
        pixels.listen()
        status_ui.status('listening')
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        try:
            if alarm == True:
               alarm = False
               assistant.stop_conversation()
               alarm_time = text
               setAlarm(alarm_time)
            elif run == True:
                run = False
                assistant.stop_conversation()
                logRun(text)
            elif text == 'power off':
                assistant.stop_conversation()
                power_off_pi()
            elif text == 'reboot':
                assistant.stop_conversation()
                reboot_pi()
            elif text == 'reboot dashboard':
               assistant.stop_conversation()
               subprocess.call("rsh pi@192.168.7.57 sudo reboot", shell=True)
            elif text == 'refresh dashboard':
               assistant.stop_conversation()
               subprocess.call("rsh pi@192.168.7.57 /home/pi/scripts/refresh.sh", shell=True)
            elif text == 'ip address':
                assistant.stop_conversation()
                say_ip()
            elif 'load' in text and 'playlist' in text:
                assistant.stop_conversation()
                textArr = text.split(" ")
                loadPlaylist(textArr[1])
            elif text == 'play music':
                assistant.stop_conversation()
                play_song()
            elif text == 'stop music':
                assistant.stop_conversation()
                stop_song()
            elif text == 'next song':
                assistant.stop_conversation()
                next_song()
            elif text == 'previous song':
                assistant.stop_conversation()
                subprocess.call("rsh pi@192.168.7.57 mpc prev", shell=True)
            elif "volume" in text:
                assistant.stop_conversation()
                volume = text.split(" ")[-1]
                subprocess.call("rsh pi@192.168.7.57 mpc volume "+volume, shell=True)
                print("Volume set to "+volume)
            elif "shuffle" in text:
                assistant.stop_conversation()
                subprocess.call("rsh pi@192.168.7.57 mpc shuffle", shell=True)
            elif text == 'time for bed':
                try:
                    assistant.stop_conversation()
                    subprocess.call("rsh jaskarnjagpal@192.168.7.23 pmset displaysleepnow", shell=True)
                    subprocess.call("rsh pi@192.168.7.57 /home/pi/scripts/hdmi-off.sh", shell=True)
                    assistant.stop_conversation()
                #speak("'Have a good night'")
                except: playError()
            elif text == 'Good morning' or text == 'wake up':
                assistant.stop_conversation()
                subprocess.call("rsh pi@192.168.7.57 /home/pi/scripts/hdmi-on.sh", shell=True)
                subprocess.call("rsh jaskarnjagpal@192.168.7.23 caffeinate -u -t 2", shell=True)
                assistant.stop_conversation()
            elif 'set an alarm' in text:
                assistant.stop_conversation()
                alarm = True
                alarmTime()
                #status_ui.status('listening')
                assistant.start_conversation()
            elif text == 'start morning alarm':
                assistant.stop_conversation()
                subprocess.call("rsh pi@192.168.7.57 python /home/pi/scripts/alarm/getWeather.py", shell=True)
            elif "off" in text and "dashboard" in text:
                assistant.stop_conversation()
                subprocess.call("rsh pi@192.168.7.57 /home/pi/scripts/hdmi-off.sh", shell=True)
            elif "on" in text and "dashboard" in text:
                assistant.stop_conversation()
                subprocess.call("rsh pi@192.168.7.57 /home/pi/scripts/hdmi-on.sh", shell=True)
            elif text == "record my run":
                try:
                    assistant.stop_conversation()
                    subprocess.call("mpg321 /home/pi/sounds/run.mp3", shell=True)
                    run = True
                    assistant.start_conversation()
                except:
                    playError();
            elif text == "delete last run" or text == "remove last run":
                assistant.stop_conversation()
                removeLastRun()
            elif text == "show me my running log" or text == "show running log":
                try:
                    assistant.stop_conversation()
                    showRunningLog()
                except:
                    playError()
            elif text == "hide running log" or text == "hide my running log" or text == "close running log":
                try:
                    assistant.stop_conversation()
                    hideRunningLog()
                except:
                    playError();
        except:
            playError()

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        pixels.think()
        status_ui.status('thinking')
    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        pixels.wakeup()
        status_ui.status('ready')
    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        subprocess.call("sudo reboot", shell=True)
        #sys.exit(1)


def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


class Pixels:
    PIXELS_N = 12

    def __init__(self, pattern=AlexaLedPattern):
        self.pattern = pattern(show=self.show)

        self.dev = apa102.APA102(num_led=self.PIXELS_N)
        
        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            self.put(self.pattern.listen)

    def think(self):
        self.put(self.pattern.think)

    def speak(self):
        self.put(self.pattern.speak)

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()

pixels = Pixels()

if __name__ == '__main__':
    main()

