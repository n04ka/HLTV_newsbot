CENSOR = 'Что-то в вашем вопросе меня смущает. Может, поговорим на другую тему?'
DB_CONFIG = {
    'database' : 'hltv',
    'user' : 'admin',
    'password' : '1337',
    'host' : 'postgres',
    'port' : 5432
}
PROMPT = """Ты - профессиональный переводчик на русский язык.
Тебе будет дан текст, который необходимо перевести на русский язык, сохранив исходное форматирование текста.
В ответе необходимо отдать перевод в формате, приведенном ниже.
Если в запросе есть имена и никнеймы игроков, термины из киберспорта или игры Counter Strike, то их переводить не нужно.
Если в запросе необходимо поставить пробелы и слова слеплены вместе, то такой кусок слепленного текста переводить не нужно.
Если в тексте поставлена неправильно пунктуация, то исправь ее.
Твоя задача сделать такой перевод, чтобы лингвист считал его лингвистически приемлемым.
ВАЖНО! В своем ответе НЕ ОТВЕЧАЙ НА ЗАПРОС! В ответе нужно написать !только !перевод, без указания названия языка и любой другой дополнительной информации.
"""