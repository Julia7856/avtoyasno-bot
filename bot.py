import telebot
from telebot import types

BOT_TOKEN = '8842420512:AAGx9TVeAfALatDMioaRWaRvM3vcl29zFQ0'
bot = telebot.TeleBot(BOT_TOKEN)

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔍 Поиск', '🚗 Марки', '📍 Запчасти', 'ℹ️ О проекте')
    return markup

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 
        "🚗 Добро пожаловать в АвтоЯсно!\n\nВыберите раздел:", 
        reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '🔍 Поиск')
def search(message):
    bot.send_message(message.chat.id, "🔍 Напишите код ошибки или опишите проблему.")

@bot.message_handler(func=lambda m: m.text == '🚗 Марки')
def brands(message):
    bot.send_message(message.chat.id, "🚗 Марки: Chery, Haval, Geely, Changan, BAIC")

@bot.message_handler(func=lambda m: m.text == '📍 Запчасти')
def parts(message):
    bot.send_message(message.chat.id, "📍 Напишите: Марка + Запчасть + Год")

@bot.message_handler(func=lambda m: m.text == 'ℹ️ О проекте')
def about(message):
    bot.send_message(message.chat.id, "ℹ️ АвтоЯсно — помощник для китайских авто.")

if __name__ == '__main__':
    bot.infinity_polling()
