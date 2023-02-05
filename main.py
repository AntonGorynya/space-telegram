import requests
import os
import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv


NASA_URL = 'https://api.nasa.gov/planetary/apod'
NASA_EPIC_URL = 'https://api.nasa.gov/EPIC/api/natural/images'
NASA_EPIC_PIC_URL = 'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image}.png'
LATEST_LAUNCH_URL = 'https://api.spacexdata.com/v5/launches/latest'
ONE_LAUNCH_URL = 'https://api.spacexdata.com/v5/launches/{id}'


def download_pick(url, path):
    folder, img_name = os.path.split(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_launch_id(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['id']


def get_image_list_spacex(launch_id):
    response = requests.get(ONE_LAUNCH_URL.format(id=launch_id))
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


def fetch_spacex_by_id(launch_id):
    for count, url in enumerate(get_image_list_spacex(launch_id)):
        download_pick(url, f'./images/spacex_{count}.jpg')


def fetch_spacex_last_launch(latest_launch_url):
    response = requests.get(latest_launch_url)
    response.raise_for_status()
    for count, url in enumerate(
            response.json()['links']['flickr']['original']):
        download_pick(url, f'./images/spacex_{count}.jpg')


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


def fetch_nasa(nasa_url, nasa_key):
    img_list = get_image_list_nasa(nasa_url, nasa_key)
    for count, url in enumerate(img_list):
        extension = get_file_extension(url)
        download_pick(url, f'./images/nasa_{count}{extension}')


def fetch_epic_nasa(nasa_url, nasa_key):
    img_list = get_image_list_epic_nasa(nasa_url, nasa_key)
    for count, url in enumerate(img_list):
        download_pick(url, f'./images/nasa_epic_{count}.png')


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_KEY']
    fetch_spacex_by_id('5eb87d47ffd86e000604b38a')
    fetch_spacex_last_launch(LATEST_LAUNCH_URL)
    fetch_nasa(NASA_URL, nasa_key)
    fetch_epic_nasa(NASA_EPIC_URL, nasa_key)
