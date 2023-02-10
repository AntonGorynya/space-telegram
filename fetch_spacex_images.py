import requests
import argparse
from common_functions import download_image


LATEST_LAUNCH_URL = 'https://api.spacexdata.com/v5/launches/latest'
ONE_LAUNCH_URL = 'https://api.spacexdata.com/v5/launches/{id}'


def get_images_spacex(launch_id):
    response = requests.get(ONE_LAUNCH_URL.format(id=launch_id))
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


def fetch_spacex_by_id(launch_id):
    for index, url in enumerate(get_images_spacex(launch_id)):
        download_image(url, f'./images/spacex_{index}.jpg')


def fetch_spacex_last_launch(latest_launch_url):
    response = requests.get(latest_launch_url)
    response.raise_for_status()
    img_meta = response.json()['links']['flickr']['original']
    for index, url in enumerate(img_meta):
        download_image(url, f'./images/spacex_{index}.jpg')


def create_parser():
    parser = argparse.ArgumentParser(description='SpaceX photo downloader')
    parser.add_argument('--id', help='launch id')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.id:
        fetch_spacex_by_id(args.id)
    else:
        fetch_spacex_last_launch(LATEST_LAUNCH_URL)
