import telebot
from telebot import util
from external import DB
from secrets import API_KEY, DEV_CHANNEL_ID


class NewsBot:
    
    def __init__(self) -> None:
        self.bot = telebot.TeleBot(API_KEY, parse_mode=None)
        self.db = DB()


    def post_message(self, id: int) -> None:
        art = self.db.get_article(id)
        images = self.db.get_article_images(id)
        text = f'<strong>⚡{art.title}⚡</strong>\n<i>{art.description}</i>\n\n{art.content}\n\n<i>Автор: {art.author}</i>'
        caption, *other = util.smart_split(text, chars_per_string=1024)
        splitted_text = util.smart_split(''.join(other), chars_per_string=4000)
        self.bot.send_photo(DEV_CHANNEL_ID, photo=images[0] if images else 'logo.jpg', caption=caption, parse_mode='html')
        for part in splitted_text:
            self.bot.send_message(DEV_CHANNEL_ID, text=part, parse_mode='html')


