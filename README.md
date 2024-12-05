# HLTV_newsbot
 Телеграмм бот, который берёт новости с HLTV.org, переводит их на русский язык с помощью Gigachat и постит в [телеграм канал](https://t.me/HLTV_newsbot_dev).
 
![hltv logo](HLTV_tg_bot/logo.jpg)

# Составляющие:
1. *Fetcher* - selenium + undetected_chromedriver + selenium_stealth + BeautifulSoup
2. *Translator* - FastAPI + GigaChat
3. *TG_bot* - FastAPI + telebot
4. *ArticleDB* - postgres
