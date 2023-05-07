import os
import requests
from urllib.parse import urlparse
from common_functions import download_image, read_db
from dotenv import load_dotenv


NASA_URL = 'https://api.nasa.gov/planetary/apod'


def get_file_extension(url):
    path = urlparse(url).path
    path, extension = os.path.splitext(path)
    return extension


def get_images_nasa(nasa_url, nasa_key, img_limit=30):
    params = {'api_key': nasa_key, 'count': img_limit}
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    images = {}
    for img_meta in response.json():
        if img_meta['media_type'] == 'image':
            img_description = img_meta['explanation'].replace('\"', ' ').replace('\'', ' ')
            images.update({img_meta['url']: img_description})
    return images


def fetch_nasa(nasa_url, nasa_key, img_limit=30):
    image_descriptions = read_db()
    images = get_images_nasa(nasa_url, nasa_key, img_limit=img_limit)
    for index, url in enumerate(images):
        extension = get_file_extension(url)
        img_name = f'nasa_{index}{extension}'
        download_image(url, f'./images/{img_name}')
        description = images[url]
        image_descriptions.update({img_name: description})
    with open('./images/db.txt', 'w') as file:
        file.write(str(image_descriptions).replace("\'", "\""))


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_KEY']
    fetch_nasa(NASA_URL, nasa_key)
