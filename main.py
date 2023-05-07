import telegram
import os
import random
import time
import argparse
from fetch_nasa_images import get_images_nasa, NASA_URL
from fetch_nasa_epic_images import NASA_EPIC_URL, get_images_epic_nasa
from fetch_spacex_images import LATEST_LAUNCH_URL
import requests
from dotenv import load_dotenv


def send_photo_loop(bot, delay_h=4):
    services = ['NASA', 'NASA_EPIC', 'SPACE_X']
    while True:
        service = random.choice(services)
        if service == 'NASA':
            images = get_images_nasa(NASA_URL, nasa_key, img_limit=8)
            image_urls = images.keys()
            for image_url in image_urls:
                bot.send_photo(chat_id=chat_id, photo=image_url, caption=images[image_url])
                time.sleep(60 * 60 * delay_h)
        if service == 'NASA_EPIC':
            images = get_images_epic_nasa(NASA_EPIC_URL, nasa_key, img_limit=1)
            for image_url in images:
                bot.send_photo(chat_id=chat_id, photo=image_url, caption='Фоточки Земли ^-^')
                time.sleep(60 * 60 * delay_h)
        if service == 'SPACE_X':
            response = requests.get(LATEST_LAUNCH_URL)
            response.raise_for_status()
            img_meta = response.json()
            image_url = img_meta['links']['flickr']['original']
            img_description = img_meta['links']['reddit']['launch']
            if image_url:
                bot.send_photo(chat_id=chat_id, photo=image_url, caption=f'Последний запуск SPACE_X {img_description}')
                time.sleep(60 * 60 * delay_h)

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
        send_photo_loop(bot, delay_h=args.d)
