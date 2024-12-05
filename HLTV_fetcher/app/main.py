from parser import Parser
from external import *
from utils import extract_id_from_url
import requests
import logging
from time import sleep


def enable_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # fileHandler = logging.FileHandler('logs.log')
    # logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # fileHandler.setFormatter(logFormatter)
    # logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    logFormatter = logging.Formatter('%(levelname)s - %(message)s')
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)


def get_db() -> DB:
     while True:
        try:
            return DB()
        except psycopg2.OperationalError as e:
            logging.warning(e)


def fetch(parser: Parser, db: DB):
    while not parser.check_connection():
            logging.error('Cannot reach HLTV.org! Retrying in 5 seconds...')
            sleep(5)
            continue
        
    parser.accept_cookies()
    
    logging.info('Fetching news...')
    parsed_news = set(db.get_article_ids())
    news = [url for url in parser.get_news() 
            if '#' not in url
            and extract_id_from_url(url) not in parsed_news]
    logging.info(f'Suitable news found: {len(news)}')
    
    for url in news:
        logging.info(f'Parsing {url}')
        try:
            art, images = parser.parse_article(url)
            logging.info(f'Succefully parsed {url}')
            db.insert_article(art)
            for img_url in images:
                db.insert_image(art.id, img_url)
            logging.info(f'Inserted article with id = {art.id}')
            requests.post(url='http://translator:80/translate', params={'id' : art.id})
        except Exception as e:
            logging.error('Parsing failed. Reason:', e)
            
    logging.info(f'All news parsed. Sleeping...')

if __name__ == '__main__':
    enable_logging()
    while True:
        fetch(parser=Parser(), db=get_db())