import telebot
import configu
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from configu import TOKEN
from telegram.ext import Filters
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
import pandas as pd

Options = dict()
Options["Choose_state_for_statisctics"] = False
Options['Shift'] = 0
BUTTON1 = "2_days"
BUTTON2 = "7_days"
BUTTON3 = "10_days"
BUTTON4 = "1"
BUTTON5 = "2"
BUTTON6 = "3"
BUTTON7 = "4"
BUTTON8 = "5"
BUTTON9 = "6"
BUTTON10 = "7"
BUTTON11 = "8"
BUTTON12 = "9"
BUTTON13 = "10"

TITLES = {
    BUTTON1: "2 DAYS", BUTTON2:"7 DAYS", BUTTON3:"10 DAYS", BUTTON4:"2020-05-26", BUTTON5:"2020-05-27",
    BUTTON6:"2020-05-28", BUTTON7:"2020-05-29", BUTTON8:"2020-05-30", BUTTON9:"2020-06-01", BUTTON10:"2020-06-02",
    BUTTON11:"2020-06-03", BUTTON12:"2020-06-04", BUTTON13:"2020-06-05",
}

def read_data():
    df = pd.read_excel('Input.xlsx')
    return  df

def do_start(bot: Bot, update:Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text = "Hello!!"
    )

def do_echo(bot: Bot, update:Update):
    text = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text = text,
    )

def day_keyboard():
    new_keyboard = [
        [
            InlineKeyboardButton(TITLES[BUTTON1], callback_data=BUTTON1),
            InlineKeyboardButton(TITLES[BUTTON2], callback_data=BUTTON2),
            InlineKeyboardButton(TITLES[BUTTON3], callback_data=BUTTON3),
        ],
        [
            InlineKeyboardButton(TITLES[BUTTON4], callback_data=BUTTON4),
            InlineKeyboardButton(TITLES[BUTTON5], callback_data=BUTTON5),
            InlineKeyboardButton(TITLES[BUTTON6], callback_data=BUTTON6),
        ],
        [
            InlineKeyboardButton(TITLES[BUTTON7], callback_data=BUTTON7),
            InlineKeyboardButton(TITLES[BUTTON8], callback_data=BUTTON8),
            InlineKeyboardButton(TITLES[BUTTON9], callback_data=BUTTON9),
        ],
        [
            InlineKeyboardButton(TITLES[BUTTON10], callback_data=BUTTON10),
            InlineKeyboardButton(TITLES[BUTTON11], callback_data=BUTTON11),
            InlineKeyboardButton(TITLES[BUTTON12], callback_data=BUTTON12),
        ],
        [
            InlineKeyboardButton(TITLES[BUTTON13], callback_data=BUTTON13),
        ],
    ]
    return InlineKeyboardMarkup(new_keyboard)

def corona_stats_dynamics(bot: Bot, update: Updater):
    chat_id = update.message.chat_id
    text = "Dynamics of virus spread"
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=day_keyboard())

def keyboard_handler(bot: Bot, update: Update, chat_data = None):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_message.chat_id
    if data == BUTTON1:
        """
        bot.send_message(
            chat_id=chat_id,
            text = "Enter the state name"
        )
        text = update.message
        query.edit_message_text(
            chat_id=update.message.chat_id,
            text= text + '-State'
        )
        print(text)
        """
        df = read_data()
        state = df['Alabama'].tolist()
        answer = "Prediction in the next 2 days:\n"
        answer += "2020-05-26: " + str(state[0]) + '\n'
        answer += "2020-05-27: " + str(state[1]) + '\n'
        bot.send_message(
            chat_id=chat_id,
            text=answer
        )

def main():
    bot = Bot(
        token=TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    corona_handler = CommandHandler('corona', corona_stats_dynamics)
    #message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(CallbackQueryHandler(callback=keyboard_handler, pass_chat_data=True))
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(corona_handler)

    updater.start_polling()
    updater.idle()

if __name__== '__main__':
    main()