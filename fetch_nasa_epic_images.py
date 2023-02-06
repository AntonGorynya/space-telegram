import requests
import datetime
import os
from common_functions import download_pick
from urllib.parse import urlparse
from dotenv import load_dotenv

NASA_EPIC_URL = 'https://api.nasa.gov/EPIC/api/natural/images'
NASA_EPIC_PIC_URL = 'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image}.png'


def get_image_list_epic_nasa(epic_nasa_url, nasa_key):
    max_index = 4
    response = requests.get(epic_nasa_url, params={'api_key': nasa_key}).json()
    image_list = []
    for count, image_data in enumerate(response):
        date = datetime.datetime.strptime(
            image_data['date'],
            '%Y-%m-%d %H:%M:%S'
        ).strftime('%Y/%m/%d')
        image = image_data['image']
        parsed_img_url = urlparse(
            NASA_EPIC_PIC_URL.format(date=date, image=image)
        )
        img_url = parsed_img_url._replace(query=f'api_key={nasa_key}').geturl()
        image_list.append(img_url)
        if max_index <= count:
            break
    return image_list


def fetch_epic_nasa(nasa_url, nasa_key):
    img_list = get_image_list_epic_nasa(nasa_url, nasa_key)
    for count, url in enumerate(img_list):
        download_pick(url, f'./images/nasa_epic_{count}.png')


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_KEY']
    fetch_epic_nasa(NASA_EPIC_URL, nasa_key)
