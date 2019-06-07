import speech_recognition as sr
import os
import re
import pyaudio
import sys
import emoji
import wolframalpha
import webbrowser
import requests
import youtube_dl
import wikipedia
import random
import time
import pyaudio
import subprocess
import vlc
import pyttsx3
import datetime
import playsound
from twilio.rest import Client
engine=pyttsx3.init()
engine.say("Welcome sir")
engine.runAndWait()
# account_sid = 'AC7504911dbd847700d6f86a438d75a99f'
# auth_token = '241329502f99b4b9772279fad0b6a807'
# client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#                               from_='whatsapp:+14155238886',
#                               body='Your Yummy Cupcakes Company order of 1 dozen frosted cupcakes has shipped and should be delivered on July 10, 2019. Details: http://www.yummycupcakes.com/',
#                               to='whatsapp:+917906224093'
#                           )

# print(message.sid)
def wolfram(search):
    app_id = "53LKA6-QRALH3RGXQ"
    client = wolframalpha.Client(app_id)
    res = client.query(search)
    ans = next(res.results).text
    return ans
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command
def response(audio):
    engine.say(audio)
    engine.runAndWait()
def assistant(command):
    print("I am here")
    if "open" in command:
        m=re.search('open(.+)',command)
        mi=m.group(1)
        mi=mi[1:]
        url = 'https://www.' + mi+'.com'
        print("Redirecting to",url)
        webbrowser.open(url)
        print("done")
        response(mi+" has been opened for you sir")
    elif 'time' in command:
        now=datetime.datetime.now()
        response('Current time is %d hours %d minutes'%(now.hour,now.minute))
    elif 'song' in command:
        print("Playing a song")
        response('Which song sir enter name and duration of play')
        k=input()
        x=int(input())
        for i in os.listdir(os.getcwd()+'/songs'):
            if k in i:
                song=vlc.MediaPlayer('songs/'+i)
                song.play()
                timeout=time.time()+x
                print(timeout,time.time())
                while True:
                    if time.time()>timeout:
                        song.stop()
                        break
        print("song played")
    elif 'hello' in command:
        response(random.choice(list(open('greetings.txt','r'))))
    elif 'joke' in command:
        print(random.choice(list(open('jokes.txt','r'))),"\U0001F923","\U0001F923")
    elif 'photo' in command:
        os.system('streamer -f jpeg -o photos/pic.jpeg')
        response('Photo taken')
    else:
        try:
            ans=wolfram(command)
            print(ans)
            response(ans)
        except:
            url=f"https://www.google.com/search?q={command}&source=lnms&sa=X&ved=0"
            webbrowser.open(url)


while True:
    assistant(myCommand())
