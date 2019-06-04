import speech_recognition as sr
import os
import re
import pyaudio
import sys
import webbrowser
import requests
import youtube_dl
import wikipedia
import random
import pyaudio
import pyttsx3
import datetime
from twilio.rest import Client
engine = pyttsx3.init()
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
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command


def response(audio):
    engine.say(audio)
    engine.runAndWait()


def assistant(command):
    print("I am here")
    if "open" in command:
        m = re.search('open(.+)', command)
        mi = m.group(1)
        mi = mi[1:]
        url = 'https://www.' + mi+'.com'
        print("Redirecting to", url)
        webbrowser.open(url)
        print("done")
        response(mi+" has been opened for you sir")
    elif 'time' in command:
        now = datetime.datetime.now()
        response('Current time is %d hours %d minutes' %
                 (now.hour, now.minute))
    else:
        response(
            'This function is currently beyond my ability but I will soon learn it')


while True:
    assistant(myCommand())
