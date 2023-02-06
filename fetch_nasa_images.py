import os
import requests
from urllib.parse import urlparse
from common_functions import download_pick
from dotenv import load_dotenv


NASA_URL = 'https://api.nasa.gov/planetary/apod'


def get_file_extension(url):
    path = urlparse(url).path
    path, extension = os.path.splitext(path)
    return extension


def get_image_list_nasa(nasa_url, nasa_key):
    img_limit = 30
    response = requests.get(
        nasa_url,
        params={
            'api_key': nasa_key,
            'count': img_limit
        }
    ).json()
    image_list = [img_data['url']
                  for img_data in response
                  if img_data['media_type'] == 'image'
                 ]
    return image_list


def fetch_nasa(nasa_url, nasa_key):
    img_list = get_image_list_nasa(nasa_url, nasa_key)
    for count, url in enumerate(img_list):
        extension = get_file_extension(url)
        download_pick(url, f'./images/nasa_{count}{extension}')


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_KEY']
    fetch_nasa(NASA_URL, nasa_key)
