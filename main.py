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



while True:
    assistant(myCommand())
