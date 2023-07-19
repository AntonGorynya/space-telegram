import telegram
import os
import sys
import random
import time
import argparse
from fetch_nasa_images import get_images_nasa, NASA_URL
from fetch_nasa_epic_images import NASA_EPIC_URL, get_images_epic_nasa
from fetch_spacex_images import LATEST_LAUNCH_URL
from xkcd import get_max_comic_num, get_xkcd_comic
import requests
from dotenv import load_dotenv


class EmptyUrlError(TypeError):
    pass

def send_photo(bot):
    services = ['NASA', 'NASA', 'NASA', 'NASA', 'NASA_EPIC', 'SPACE_X', 'XKCD']
    service = random.choice(services)

    if service == 'NASA':
        images = get_images_nasa(NASA_URL, nasa_key, img_limit=1)
        image_urls = images.keys()
        for image_url in image_urls:
            image_description = (images[image_url][:1022] + '..') if len(images[image_url]) > 1024 else images[image_url]
            bot.send_photo(chat_id=chat_id, photo=image_url, caption=image_description)

    if service == 'NASA_EPIC':
        images = get_images_epic_nasa(NASA_EPIC_URL, nasa_key, img_limit=1)
        for image_url in images:
            bot.send_photo(chat_id=chat_id, photo=image_url, caption='Фоточки Земли ^-^')

    if service == 'SPACE_X':
        response = requests.get(LATEST_LAUNCH_URL)
        response.raise_for_status()
        img_meta = response.json()
        image_url = img_meta['links']['flickr']['original']
        img_description = img_meta['links']['reddit']['launch']
        if image_url:
            bot.send_photo(chat_id=chat_id, photo=image_url, caption=f'Последний запуск SPACE_X {img_description}')
        else:
            raise EmptyUrlError

    if service == 'XKCD':
        max_comic_num = get_max_comic_num()
        img_meta = get_xkcd_comic(id=random.randint(0, max_comic_num))
        img_description = img_meta['alt']
        img_name = img_meta['img']
        bot.send_photo(chat_id=chat_id, photo=img_name, caption=f'{img_description}')


def create_parser():
    parser = argparse.ArgumentParser(
        description='upload photo to telegram chanel'
    )
    parser.add_argument('-d', help='delay in hours', default=4)
    parser.add_argument('-p', help='path to photo')
    return parser


if __name__ == '__main__':
    load_dotenv()
    nasa_key = os.environ['NASA_KEY']
    telegram_token = os.environ['TG_TOKEN']
    chat_id = os.environ['CHAT_ID']
    bot = telegram.Bot(token=telegram_token)
    parser = create_parser()
    args = parser.parse_args()
    if args.p:
        with open(args.p, 'rb') as file:
            bot.send_photo(chat_id=chat_id, photo=file)
    else:
        while True:
            try:
                send_photo(bot)
                time.sleep(60 * 60 * args.d)
            except requests.exceptions.ConnectionError as error:
                print(error, file=sys.stderr)
                print('Trying to reconnect over 30 seconds...')
                time.sleep(30)
            except telegram.error.BadRequest as error:
                print(error, file=sys.stderr)
            except EmptyUrlError as error:
                print(error, file=sys.stderr)
            except requests.exceptions.HTTPError as error:
                print(error, file=sys.stderr)