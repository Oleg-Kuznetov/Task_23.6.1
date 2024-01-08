import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу, введите команду боту в следующем формате: '
            '\n<имя валюты, цену которой необходимо узнать> <имя валюты, '
            'в которой надо узнать цену первой валюты> <количество первой '
            'валюты>\nСписок всех доступных валют: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) > 3:
            raise APIException('Слишком много параметров!')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров!')
        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос!\n{e}')
    else:
        text = f'Стоимость {amount} {base} = {total_base} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)