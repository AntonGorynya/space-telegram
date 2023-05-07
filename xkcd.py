import requests
import os
import random
from common_functions import  download_image

XKCD_IMG_URL = 'https://xkcd.com/{id}/info.0.json'


def get_xkcd_comic(id=1):
    response = requests.get(XKCD_IMG_URL.format(id=id))
    response.raise_for_status()
    return response.json()


def get_xkcd_random_comic(max_comic_num):
    img_meta = get_xkcd_comic(id=random.randint(0, max_comic_num))
    img_description = img_meta['alt']
    img_name = os.path.basename(img_meta['img'])
    download_image(img_meta['img'], img_name)
    return img_name, img_description


def get_max_comic_num():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()['num']