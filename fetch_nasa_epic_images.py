import requests
import datetime
import os
from common_functions import download_image
from urllib.parse import urlparse
from dotenv import load_dotenv

NASA_EPIC_URL = 'https://api.nasa.gov/EPIC/api/natural/images'
NASA_EPIC_PIC_URL = 'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image}.png'


def get_images_epic_nasa(epic_nasa_url, nasa_key, img_limit=4):
    response = requests.get(epic_nasa_url, params={'api_key': nasa_key})
    response.raise_for_status()
    images = []
    for index, image_meta in enumerate(response.json()):
        date = datetime.datetime.strptime(
            image_meta['date'],
            '%Y-%m-%d %H:%M:%S'
        ).strftime('%Y/%m/%d')
        image = image_meta['image']
        parsed_img_url = urlparse(
            NASA_EPIC_PIC_URL.format(date=date, image=image)
        )
        img_url = parsed_img_url._replace(query=f'api_key={nasa_key}').geturl()
        images.append(img_url)
        if img_limit <= index+1:
            break
    return images


def fetch_epic_nasa(nasa_url, nasa_key, img_limit=4):
    images = get_images_epic_nasa(nasa_url, nasa_key, img_limit=img_limit)
    for index, url in enumerate(images):
        download_image(url, f'./images/nasa_epic_{index}.png')


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_KEY']
    fetch_epic_nasa(NASA_EPIC_URL, nasa_key)
