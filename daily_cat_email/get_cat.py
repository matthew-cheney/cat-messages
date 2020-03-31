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
