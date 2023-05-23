import telebot
from config import keys, TOKEN
from utils import CurrencyConverter, ConvertException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message) -> str:
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\
Список доступных валют:  /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message) -> str:
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message) -> str:
    values = message.text.split(' ')  # сначала переносим параметры в список

    if len(values) != 3:  # проверка на число введенных параметров
        raise ConvertException('Неверное число параметров')

    quote, base, amount = values  # распаковываем список
    total_base = CurrencyConverter.converter(quote, base, amount)
    text = f'{amount} {keys[quote]} ({quote}) = {total_base} {keys[base]} ({base})'
    bot.send_message(message.chat.id, text)


# @bot.message_handler()
# def echo_test(message: telebot.types.Message):
#     if 'биткоин'.casefold() in message.text:
#         txt = 'биткоин'
#         bot.send_message(message.chat.id, f"Привет! Да, у меня есть {txt}")
#     else:
#         bot.reply_to(message, 'Нет, извини, нету...')


bot.polling(non_stop=True)
