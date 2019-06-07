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
from os.path import isdir, isfile, exists, basename
from re import search, IGNORECASE
from subprocess import Popen, run, PIPE
from sys import argv
import argparse
import logging
from magic import from_file
from twilio.rest import Client
engine = pyttsx3.init()
engine.say("Welcome sir")
engine.runAndWait()
# account_sid = '###########'
# auth_token = '############'
# client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#                               from_='whatsapp:+14155238886',
#                               body='Your Yummy Cupcakes Company order of 1 dozen frosted cupcakes has shipped and should be delivered on July 10, 2019. Details: http://www.yummycupcakes.com/',
#                               to='whatsapp:+917906224093'
#                           )
# print(message.sid)

filetypes = {
    r'\.(pdf|epub)$': ['mupdf'],
    r'\.(txt|tex|md|rst|py|sh)$': ['gvim', '--nofork'],
    r'\.html$': ['firefox'],
    r'\.xcf$': ['gimp'],
    r'\.e?ps$': ['gv'],
    r'\.(jpe?g|png|gif|tiff?|p[abgp]m|bmp|svg)$': ['gpicview'],
    r'\.(pax|cpio|zip|jar|ar|xar|rpm|7z)$': ['tar', 'tf'],
    r'\.(tar\.|t)(z|gz|bz2?|xz)$': ['tar', 'tf'],
    r'\.(mp4|mkv|avi|flv|mpg|movi?|m4v|webm|vob)$': ['mpv'],
    r'\.(s3m|xm|mod|mid)$':
    ['urxvt', '-title', 'Timidity++', '-e', 'timidity', '-in', '-A30a']
}
othertypes = {'dir': ['rox'], 'txt': ['gvim', '--nofork']}


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
    elif 'file' in command:
        engine.say('Which file sir')
        engine.runAndWait()
        files = myCommand()
        for nm in files:
            logging.info(f"trying '{nm}'")
            if isdir(nm):
                cmds = othertypes['dir'] + [nm]
            elif isfile(nm):
                cmds = matchfile(filetypes, othertypes, nm)
            else:
                cmds = None

            if not cmds:
                logging.warning(f"do not know how to open '{nm}'")
                continue
            try:
                Popen(cmds)
            except OSError as e:
                logging.error("Cant open")
    elif 'app' in command:
        engine.say('Which app sir')
        engine.runAndWait()
        appname = myCommand()
        Popen("appname")
    else:
        response(
            'This function is currently beyond my ability but I will soon learn it')


def matchfile(fdict, odict, fname):
    for k, v in fdict.items():
        if search(k, fname, IGNORECASE) is not None:
            return v + [fname]
    if b'text' in from_file(fname):
        return odict['txt'] + [fname]
    return None


def locate(args):
    files = []
    try:
        for nm in args:
            if exists(nm):
                files.append(nm)
            else:
                cp = run(['locate', nm], stdout=PIPE)
                paths = cp.stdout.decode('utf-8').splitlines()
                if len(paths) == 1:
                    files.append(paths[0])
                elif len(paths) == 0:
                    logging.warning(f"path '{nm}' not found")
                else:
                    basenames = []
                    for p in paths:
                        if basename(p) == nm:
                            basenames.append(p)
                            logging.info(f'found possible match "{p}"')
                    if len(basenames) == 1:
                        files.append(basenames[0])
                    else:
                        logging.warning(f"ambiguous path '{nm}' skipped")
                        for p in basenames:
                            logging.warning(f"found '{p}'")
    except FileNotFoundError:
        files = args
    return files


while True:
    assistant(myCommand())
