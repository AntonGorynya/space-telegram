import os
import requests
from urllib.parse import urlparse
from common_functions import download_image
from dotenv import load_dotenv


NASA_URL = 'https://api.nasa.gov/planetary/apod'


def get_file_extension(url):
    path = urlparse(url).path
    path, extension = os.path.splitext(path)
    return extension


def get_images_nasa(nasa_url, nasa_key):
    img_limit = 30
    params = {'api_key': nasa_key, 'count': img_limit}
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    images = [img_meta['url']
              for img_meta in response.json()
              if img_meta['media_type'] == 'image'
    ]
    return images


def fetch_nasa(nasa_url, nasa_key):
    images = get_images_nasa(nasa_url, nasa_key)
    for index, url in enumerate(images):
        extension = get_file_extension(url)
        download_image(url, f'./images/nasa_{index}{extension}')


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_KEY']
    fetch_nasa(NASA_URL, nasa_key)
