import requests
import json
import glob

import os

from daily_cat_email.settings import PATH_TO_DAILY_CAT

dirname = os.path.dirname(__file__)

def get_cat():
    url = "https://api.thecatapi.com/v1/images/search?mime_types=jpg"
    headers = {'user': 'matthew@cheneycreations.com'}

    r = requests.get(url=url, headers=headers)

    if r.status_code != 200:
        print("something went very wrong!")
        exit(1)

    r_content = json.loads(r.content.decode('utf-8'))
    cat_url = r_content[0]['url']

    r = requests.get(cat_url, headers=headers)

    if r.status_code != 200:
        print("something else went vey wrong!")
        exit(1)


    if r.headers.get('Content-Type') == 'image/jpeg':
        with open(PATH_TO_DAILY_CAT, 'wb') as f:
            f.write(r.content)
        return PATH_TO_DAILY_CAT
    else:
        print(r.headers.get('Content-Type'))
        return get_cat()

def get_cat_old():

    url = "https://api.thecatapi.com/v1/images/search?mime_types=jpg"
    headers = {}

    r = requests.get(url, params=headers)

    r_content = json.loads(r.content.decode(('utf-8')))

    cat_url = r_content[0]['url']

    r = requests.get(cat_url)

    all_cat_filenames = glob.glob('cat_images/cat_*')

    if r.headers.get('Content-Type') == 'image/jpeg':
        with open(f'cat_images/cat_{len(all_cat_filenames):05d}.jpg', 'wb') as f:
            f.write(r.content)
    else:
        print(r.headers.get('Content-Type'))
        return get_cat()

def show_cat():
    openImage('cat_image.jpg')

import sys
import subprocess

def openImage(path):
    imageViewerFromCommandLine = {'linux':'xdg-open',
                                  'win32':'explorer',
                                  'darwin':'open'}[sys.platform]
    subprocess.run([imageViewerFromCommandLine, path])

import PySimpleGUI as sg

def main():
    sg.theme('DarkAmber')	# Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Button('Get Cat'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):	# if user closes window or clicks cancel
            break
        if event in ('Get Cat'):
            get_cat_old()
            show_cat()

    window.close()

if __name__ == '__main__':
    main()
