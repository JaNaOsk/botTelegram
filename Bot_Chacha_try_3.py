import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! Я бот по имени Чача. Чтобы я начал работу, введите данные в следующей форме:\n<имя валюты>\
<в какую валюту перевести>\
<количество переводимой валюты>\nВы можете получить список доступных валют, нажав сюда-> /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров.')
        if len(values) < 3:
            raise ConvertionException('Слишком короткая команда. Для помощи нажмите /help')
        quote, base, amount = values
        n = float(amount)
        total_base = CryptoConverter.get_price(quote, base,amount)
        total_base=round(total_base*n,2)

    except Exception as e:
        bot.reply_to(message,f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
