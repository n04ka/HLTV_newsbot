from schemas import Article, TranslatedArticle
from config import DB_CONFIG
import psycopg2


class DB:
    
    def __init__(self) -> None:
        self.conn: psycopg2.extensions.connection = psycopg2.connect(**DB_CONFIG)


    def get_article(self, id: int) -> Article:
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""select * from article where id = %s""", (id,))
                record = cursor.fetchone()
        if not record:
            print(record)
            raise ValueError(f'No article with id = {id} in the database')
        id, title, author, timestamp, url, description, content = record
        return Article(id=id, 
                       title=title, 
                       author=author, 
                       timestamp=timestamp, 
                       url=url,
                       description=description,
                       content=content
                       )
        
        
    def insert_translated_article(self, art: TranslatedArticle):
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""insert into translation (id, title, author, description, content) values (%(id)s, %(title)s, %(author)s, %(description)s, %(content)s)""", (art.__dict__))