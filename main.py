import telebot
import re


bot = telebot.TeleBot("6788334491:AAEgFkwX-2BgwBA1cOOltrI1prRcP0iNeso")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "напиши `` чтобы начать работать с ботом")


@bot.message_handler(commands=['оценить'])
def критерий(message):
    bot.reply_to(message, "Оценка начинается.")
    bot.reply_to(message, "1. Начнем с прибыли.")
    bot.reply_to(message, "Укажите размер выручки в млн руб. за 2022 год, указанный во 2 форме бух. отчетности.")


@bot.message_handler(regexp='\\d+млн')
def echo_all(message):
    m = re.search(r'\d', message.text)
    revenue = int(m.group())
    if revenue >= 2:
        bot.send_message(message.from_user.id, "Ура! Вы проходите по критерию. Идём дальше.")
        bot.send_message(message.from_user.id, "2. Укажите численность персонала в 2022 году.")
    else:
        bot.send_message(message.from_user.id, "Менее 2млн.\nКомпания не подходит")
    # bot.send_sticker()


bot.infinity_polling()
