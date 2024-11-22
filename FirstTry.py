import telebot
import webbrowser
import logging
from telebot import types



logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot('7634177875:AAHhnscAJw-WvWobkWoyVVpLakpeXObUv1E')



@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти в группа VK')
    btn2 = types.KeyboardButton('Записать взос')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>', parse_mode='html')


@bot.message_handler(commands=['pool'])
def site(message):
    bot.send_poll(message.chat.id, question="Пример тренировки",is_anonymous=False, options=["буду", "не буду"] )

    
@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://vk.com/moscowbruins')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.reply_to(message, f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>', parse_mode='html')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID {message.from_user.id}')
    elif message.text.lower() == 'chat_id':
        bot.reply_to(message, f'ID {message.chat.id}')
    elif message.text == 'msgInfo':
        bot.send_message(message.chat.id, f'ID {message}', parse_mode='html')
    else:
        bot.send_message(2389411401, f'ID ghbdtn', parse_mode='html')




@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти в группа VK', url='https://vk.com/bruinsmsk')
    btn2 = types.InlineKeyboardButton('Записать взос', callback_data='create_check')
    markup.row(btn1, btn2)
    # markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://vk.com/moscowbruins'))
    # markup.add(types.InlineKeyboardButton('Записать взос', callback_data='create_check'))
    bot.reply_to(message, 'Спасибо!', reply_markup=markup)

# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):

# @bot.add_channel_post_handler()

bot.infinity_polling()
