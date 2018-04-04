from newsapi import NewsApiClient
import requests
import json
import urllib2
import subprocess
import codecs
import datetime

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

newsText = "Today in the news.\r\n"+article1Title+"... "+article1Desc+"\r\n..."+article2Title+"... "+article2Desc+"\r\n..."+article3Title+"..."+article3Desc+"\r\n..."+article4Title+"..."+article4Desc
print(pollyText)
text_file = open("news.txt", "w")
text_file.write(newsText)
text_file.close()

f = codecs.open("news.txt", encoding='utf-8')

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
execute_command = 'cat ' + file_names + '>newsresult.mp3'
subprocess.call(execute_command, shell=True)

execute_command = 'rm ' + file_names
print 'Removing temporary files: ' + execute_command
subprocess.call(execute_command, shell=True)
subprocess.call("mpg321 newsresult.mp3", shell=True)
