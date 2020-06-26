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
import math

Options = dict()
Options["7 DAYS"] = 0
Options["10 DAYS"] = 0
Options['Shift'] = 0
Options["2020-05-26"] = 0
Options["2020-05-27"] = 0
Options["2020-05-28"] = 0
Options["2020-05-29"] = 0
Options["2020-05-30"] = 0
Options["2020-06-01"] = 0
Options["2020-06-02"] = 0
Options["2020-06-03"] = 0
Options["2020-06-04"] = 0
Options["2020-06-05"] = 0


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


def visualisation(aspect: str, dates: list, data_set: list) -> None:
    y = data_set
    # соответствующие значения оси Y
    x = dates
    fig, ax = plt.subplots()
    ax.plot(x, y, color='r', linewidth=3)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(abs(data_set[-1] - data_set[0]) // 10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    #  Добавляем линии основной сетки:
    ax.grid(which='major', color='k')
    #  Включаем видимость вспомогательных делений:
    ax.minorticks_on()
    #  Теперь можем отдельно задавать внешний вид
    #  Вспомогательной сетки:
    ax.grid(which='minor',
            color='gray',
            linestyle=':')
    # Название оси х
    plt.xlabel('days', fontsize=15)
    # имя оси Y
    plt.ylabel(aspect, fontsize=15)

    fig.set_figwidth(12)
    fig.set_figheight(8)

    plt.savefig('graphic')
    plt.clf()

def read_data():
    df = pd.read_excel('Input.xlsx')
    return  df

def chat_help(bot: Bot, update:Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text = "Hello, please enter /corona to start prediction"
    )

def corona_stats_states(bot: Bot, update:Update):
    chat_id = update.message.chat_id
    if not (Options["Shift"] or Options["7 DAYS"] or Options['10 DAYS'] or Options["2020-05-26"] or Options["2020-05-27"] or Options["2020-05-28"]\
            or Options["2020-05-29"] or Options["2020-05-30"] or Options["2020-06-01"] or Options["2020-06-02"] or Options["2020-06-03"] or Options["2020-06-04"] or Options["2020-06-05"]):
        text = update.message.text
        bot.send_message(
            chat_id=chat_id,
            text='Please, write correct name'
        )
    elif Options["Shift"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction "  + str(text) + " in the next 2 days:\n"
        answer += "2020-05-26: " + str(math.ceil(state[0])) + '\n'
        answer += "2020-05-27: " + str(math.ceil(state[1])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["Shift"] = 0
        return

    elif Options["7 DAYS"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction " + str(text) +" in the next 7 days:\n"
        answer += "2020-05-26: " + str(math.ceil(state[0])) + '\n'
        answer += "2020-05-27: " + str(math.ceil(state[1])) + '\n'
        answer += "2020-05-28: " + str(math.ceil(state[2])) + '\n'
        answer += "2020-05-29: " + str(math.ceil(state[3])) + '\n'
        answer += "2020-05-30: " + str(math.ceil(state[4])) + '\n'
        answer += "2020-05-01: " + str(math.ceil(state[5])) + '\n'
        answer += "2020-05-02: " + str(math.ceil(state[6])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["7 DAYS"] = 0
        return
    elif Options["10 DAYS"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction " + str(text) +" in the next 7 days:\n"
        answer += "2020-05-26: " + str(math.ceil(state[0])) + '\n'
        answer += "2020-05-27: " + str(math.ceil(state[1])) + '\n'
        answer += "2020-05-28: " + str(math.ceil(state[2])) + '\n'
        answer += "2020-05-29: " + str(math.ceil(state[3])) + '\n'
        answer += "2020-05-30: " + str(math.ceil(state[4])) + '\n'
        answer += "2020-05-01: " + str(math.ceil(state[5])) + '\n'
        answer += "2020-05-02: " + str(math.ceil(state[6])) + '\n'
        answer += "2020-05-03: " + str(math.ceil(state[7])) + '\n'
        answer += "2020-05-04: " + str(math.ceil(state[8])) + '\n'
        answer += "2020-05-05: " + str(math.ceil(state[9])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["10 DAYS"] = 0
        return
    elif Options["2020-05-26"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-05-26: " + str(math.ceil(state[0])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-05-26"] = 0
        return

    elif Options["2020-05-27"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-05-27: " + str(math.ceil(state[1])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-05-27"] = 0
        return

    elif Options["2020-05-28"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-05-28: " + str(math.ceil(state[2])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-05-28"] = 0
        return

    elif Options["2020-05-29"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-05-29: " + str(math.ceil(state[3])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-05-29"] = 0
        return

    elif Options["2020-05-30"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-05-30: " + str(math.ceil(state[4])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-05-30"] = 0
        return

    elif Options["2020-06-01"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-06-01: " + str(math.ceil(state[5])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-06-01"] = 0
        return

    elif Options["2020-06-02"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-06-02: " + str(math.ceil(state[6])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-06-02"] = 0
        return

    elif Options["2020-06-03"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-06-03: " + str(math.ceil(state[7])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-06-03"] = 0
        return

    elif Options["2020-06-04"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-06-04: " + str(math.ceil(state[8])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-06-04"] = 0
        return

    elif Options["2020-06-05"]:
        text = update.message.text
        df = read_data()
        state = df[text].tolist()
        answer = "Prediction for " + str(text) + "\n"
        answer += "2020-06-05: " + str(math.ceil(state[9])) + '\n'
        bot.send_message(
            chat_id=update.message.chat_id,
            text=answer
        )
        Options["2020-06-05"] = 0
        return


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

def keyboard(bot: Bot, update: Update, chat_data = None):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_message.chat_id
    if data == BUTTON1:

        bot.send_message(
            chat_id=chat_id,
            text = "Enter the state name:"
        )
        Options["Shift"] = 1

    elif data == BUTTON2:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['7 DAYS'] = 1

    elif data == BUTTON3:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['10 DAYS'] = 1

    elif data == BUTTON4:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-05-26'] = 1

    elif data == BUTTON5:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-05-27'] = 1

    elif data == BUTTON6:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-05-28'] = 1

    elif data == BUTTON7:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-05-29'] = 1

    elif data == BUTTON8:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-05-30'] = 1

    elif data == BUTTON9:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-06-01'] = 1

    elif data == BUTTON10:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-06-02'] = 1

    elif data == BUTTON11:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-06-03'] = 1

    elif data == BUTTON12:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-06-04'] = 1

    elif data == BUTTON13:
        bot.send_message(
            chat_id=chat_id,
            text="Enter the state name:"
        )
        Options['2020-06-05'] = 1

def main():
    bot = Bot(
        token=TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", chat_help)
    corona_handler = CommandHandler('corona', corona_stats_dynamics)
    message_handler = MessageHandler(Filters.text, corona_stats_states)

    updater.dispatcher.add_handler(CallbackQueryHandler(callback=keyboard, pass_chat_data=True))
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(corona_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()

if __name__== '__main__':
    main()