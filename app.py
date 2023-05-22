import telebot
import requests

TOKEN = "1680972792:AAEaZO68WjS0ZRqKXojW6Zv0j2ptxfeV_F0"

bot = telebot.TeleBot(TOKEN)

keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
    'рубль': 'RUB',
    'солана': 'SOL',
    'евро': 'EUR'
}


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\
Список доступных валют:  /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')


@bot.message_handler()
def echo_test(message: telebot.types.Message):
    if 'биткоин'.casefold() in message.text:
        txt = 'биткоин'
        bot.send_message(message.chat.id, f"Привет! Да, у меня есть {txt}")
    else:
        bot.reply_to(message, 'Нет, извини, нету...')


bot.polling(non_stop=True)
