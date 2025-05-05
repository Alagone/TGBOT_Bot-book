import json

data = {}
with open("lexicon/lexicon_ru.json", "r", encoding="UTF-8") as file:
    data = json.load(file)

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Начать беседу',
    '/beginning': 'В начало книги',
    '/continue': 'Продолжить чтение',
    '/bookmarks': 'Мои закладки',
    '/help': 'Справка по работе бота'
}