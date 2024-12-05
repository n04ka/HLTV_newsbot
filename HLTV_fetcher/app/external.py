from schemas import Article
from config import DB_CONFIG
from typing import List
import psycopg2


class DB:
    
    def __init__(self) -> None:
        self.conn: psycopg2.extensions.connection = psycopg2.connect(**DB_CONFIG)


    def get_article_ids(self) -> List[int]:
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""select id from article""")
                ids = [int(record[0]) for record in cursor.fetchall()]
        return ids


    def insert_article(self, art: Article):
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                               insert into article (id, title, author, timestamp, url, description, content)
                               values (%(id)s, %(title)s, %(author)s, %(timestamp)s, %(url)s, %(description)s, %(content)s)
                               """, (art.__dict__))
        
        
    def insert_image(self, art_id: int, url: str):
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                               insert into image (article_id, url)
                               values (%s, %s)
                               """, (art_id, url))
                
                