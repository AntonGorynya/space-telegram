import requests
import argparse
from common_functions import download_pick


LATEST_LAUNCH_URL = 'https://api.spacexdata.com/v5/launches/latest'
ONE_LAUNCH_URL = 'https://api.spacexdata.com/v5/launches/{id}'


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


def create_parser():
    parser = argparse.ArgumentParser(description='SpaceX photo downloader')
    parser.add_argument('--id', help='launch id')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    #fetch_spacex_by_id('5eb87d47ffd86e000604b38a')
    if args.id:
        fetch_spacex_by_id(args.id)
    else:
        fetch_spacex_last_launch(LATEST_LAUNCH_URL)
