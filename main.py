import telegram
import os
import random
import time
import argparse
from dotenv import load_dotenv


chat_id = '@l00k_around'


def send_photo_loop(bot, delay_h=4):
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
    parser.add_argument('-d', help='delay in hours', default=4)
    parser.add_argument('-p', help='path to photo')
    return parser


if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.environ['TELEGA_KEY']
    bot = telegram.Bot(token=telegram_token)
    parser = create_parser()
    args = parser.parse_args()
    if args.p:
        bot.send_photo(chat_id=chat_id, photo=open(args.p, 'rb'))
    else:
        send_photo_loop(bot, delay_h=args.d)
