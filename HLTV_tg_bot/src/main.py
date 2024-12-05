from fastapi import FastAPI
from bot import NewsBot


app = FastAPI(debug=True)
bot = NewsBot()


@app.post('/post')
def post_message(id: int):
    bot.post_message(id)