import telegram
import os
from dotenv import load_dotenv

chat_id = '@l00k_around'

if __name__ == '__main__':
    load_dotenv()
    bot = telegram.Bot(token=os.environ['TELEGA_KEY'])
    bot.send_message(text='Hi John!', chat_id='@l00k_around')
