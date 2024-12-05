from gigachat import GigaChat
from fastapi import FastAPI
from schemas import TranslatedArticle
from external import DB
from config import CENSOR, PROMPT
from secrets import TOKEN
import requests


app = FastAPI(debug=True)
db = DB()


@app.post('/translate')
def translate(id: int):
    art = db.get_article(id)
    
    with GigaChat(credentials=TOKEN, verify_ssl_certs=False) as giga:
        full_text = '\n\n'.join((art.title, art.description, art.content))
        response = giga.chat(f"{PROMPT}\n{full_text}")
        if CENSOR in response.choices[0].message.content:
            raise Exception(f'Gigachat censorship on article with id = {id}')
    
    title, description, content = response.choices[0].message.content.split('\n\n', maxsplit=2)
    translation = TranslatedArticle(id=art.id, title=title, author=art.author, description=description, content=content)
    db.insert_translated_article(translation)
    requests.post(url='http://bot:8000/post', params={'id' : id})
    