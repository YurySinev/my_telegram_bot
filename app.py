import telebot
import requests
import json

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


class ConvertException(Exception):
    ...


class CurrencyConverter:
    @staticmethod
    def converter(quote: str, base: str, amount: str):
        if quote == base:  # не введена ли одна и та же валюта?
            raise ConvertException(f'Нельзя перевести валюту в саму себя')

        try:  # проверка правильности написания первой валюты:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Валюта {quote} не найдена')

        try:  # и второй валюты
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Валюта {base} не найдена')

        try:  # проверка корректности введенного количества и перевод его в тип float
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # итог: базовая цена валюты * количество:
        total_base = float(json.loads(r.content)[keys[base]]) * amount

        return total_base


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
