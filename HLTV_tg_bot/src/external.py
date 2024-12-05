from typing import List
from schemas import TranslatedArticle
from config import DB_CONFIG
import psycopg2


class DB:
    
    def __init__(self) -> None:
        self.conn: psycopg2.extensions.connection = psycopg2.connect(**DB_CONFIG)


    def get_article(self, id: int) -> TranslatedArticle:
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""select * from translation where id = %s""", (id,))
                record = cursor.fetchone()
        if not record:
            print(record)
            raise ValueError(f'No article with id = {id} in the database')
        id, title, author, description, content = record
        return TranslatedArticle(id=id, 
                       title=title, 
                       author=author,
                       description=description,
                       content=content
                       )
    
    
    def get_article_images(self, id: int) -> List[str]:
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""select url from image where article_id = %s""", (id,))
                records = cursor.fetchall()
        return [record[0] for record in records]
        