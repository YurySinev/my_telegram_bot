import telebot

TOKEN = "1680972792:AAEaZO68WjS0ZRqKXojW6Zv0j2ptxfeV_F0"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
        <в какую валюту перевести> \
        <количество переводимой валюты>'
    bot.send_message(message.chat.id, text)

@bot.message_handler()
def echo_test(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Привет!")

bot.polling(non_stop=True)
