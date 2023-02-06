import telegram
import os
import random
import time
import argparse
from dotenv import load_dotenv


chat_id = '@l00k_around'


def send_photo_loop(telegram_token, delay_h=4):
    bot = telegram.Bot(token=telegram_token)
    img_list = os.listdir('./images')
    while True:
        random.shuffle(img_list)
        for pic in img_list:
            bot.send_photo(chat_id=chat_id, photo=open(f'images/{pic}', 'rb'))
            time.sleep(60 * 60 * delay_h)


def create_parser():
    parser = argparse.ArgumentParser(
        description='upload photo to telegram chanel'
    )
    parser.add_argument('--delay', help='delay in hours', default=4)
    return parser


if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.environ['TELEGA_KEY']
    parser = create_parser()
    args = parser.parse_args()
    send_photo_loop(telegram_token, delay_h=args.delay)
