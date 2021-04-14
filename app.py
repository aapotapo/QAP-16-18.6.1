import telebot

from config import TOKEN
from extensions import APIException, ExchangeRates

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/start', '/help')
    bot.send_message(message.chat.id, text=help_text(), reply_markup=keyboard)


def help_text():
    return 'Введите буквенные коды валют для конвертации и сумму\n' \
           'Например для конвертации 100 рублей в евро: RUB EUR 100\n' \
           'Список доступных валют: /values'


@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    try:
        text = 'Доступные валюты:'
        text += ', '.join(ExchangeRates.supported_symbols())
        bot.reply_to(message, text)
    except RuntimeError as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException(help_text())
        base, quote, amount = values
        result = ExchangeRates.get_price(base.upper(), quote.upper(), amount)
    except APIException as e:
        print(e)
        bot.reply_to(message, e)
    except RuntimeError as e:
        print(e)
        bot.reply_to(message, e)
    else:
        text = f"{amount} {base.upper()} в {quote.upper()} = {result}"
        print(text)
        bot.send_message(message.chat.id, text)

if __name__ == '__main__':
     bot.infinity_polling()
