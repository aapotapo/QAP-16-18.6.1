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
        from_symbol, to_symbol, amount = values
        rate = ExchangeRates.rate(from_symbol, to_symbol)
    except APIException as e:
        bot.reply_to(message, e)
    except RuntimeError as e:
        bot.reply_to(message, e)
    else:
        result = round(float(amount) * rate, 2)
        text = f"{amount} {from_symbol} в {to_symbol} = {result}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
