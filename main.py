import telegram
import os
import random
import time
import argparse
from common_functions import read_db
from dotenv import load_dotenv


def send_photo_loop(bot, delay_h=4):
    images = os.listdir('./images')
    while True:
        random.shuffle(images)
        img_meta = read_db()
        help(bot.send_photo)
        for img in images:
            with open(f'images/{img}', 'rb') as file:
                if img in img_meta:
                    bot.send_photo(chat_id=chat_id, photo=file, caption=img_meta[img])
                else:
                    bot.send_photo(chat_id=chat_id, photo=file, caption=None)
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
    telegram_token = os.environ['TELEGA_KEY']
    chat_id = os.environ['CHAT_ID']
    bot = telegram.Bot(token=telegram_token)
    parser = create_parser()
    args = parser.parse_args()
    if args.p:
        with open(args.p, 'rb') as file:
            bot.send_photo(chat_id=chat_id, photo=file)
    else:
        send_photo_loop(bot, delay_h=args.d)
