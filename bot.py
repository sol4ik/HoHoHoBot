# survey about the gift [optional] and gift search

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ChosenInlineResultHandler

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import get_items

search_keys = []
gift = ''

# buttons functions
def NewMenu(bot, chatid, options, text):
        menu = create_menu(options)
        bot.send_message(chat_id=chatid, text=text, reply_markup=menu)


def create_menu(options):
    return InlineKeyboardMarkup([[InlineKeyboardButton(i[0],
                                callback_data=i[1])
                                for i in list(options)]])


# survey results
def getsurveyres(search_keys):
    if search_keys[2] == 'ucu':
        search_keys[0], search_keys[1] = "None", "None"
    return get_items.getjsonitems(search_keys)


# bot start
def start(bot, update):
    search_keys.clear()

    bot.sendPhoto(chat_id=update.message.chat_id,
                  photo=open(('img/1.png'), 'rb'))
    NewMenu(bot, update.message.chat_id,
            [['Про-хо-хо-хо-довжити', 'cont']], text='*тиць*')


def button_press(bot, update):
    additional_button = False
    if update.callback_query.data == 'cont':
        img_path = "img/2.png"
        options = [['Авжеж', 'yes'], ['На жаль, ще ні', 'no']]
    elif update.callback_query.data == "no":
        img_path = "img/3.png"
        options = [['Про-хо-хо-хо-довжити', 'choose']]
    elif update.callback_query.data == 'yes':
        bot.sendPhoto(chat_id=update.callback_query.message.chat_id,
                      photo=open('img/11.png', 'rb'))
        bot.sendMessage(chat_id=update.callback_query.message.chat_id,
                        text="*введи свій подаруночо-хо-хо-к*")
        bot.sendMessage(chat_id=update.callback_query.message.chat_id,
                        text="Прикад: /gift книжка")
        # user inputs gift
    elif update.callback_query.data == 'choose':
        img_path = "img/4.png"
        options = [['Хлопчик', 'male'], ['Дівчинка', 'female']]
    elif update.callback_query.data in ['male', 'female']:
        search_keys.append(update.callback_query.data)
        img_path = "img/5.png"
        options = [['0-2', 'baby'], ['2-6', 'toddler'], ['6-12', 'kid'],
                   ['12-18', 'teen'], ['18-24', 'youth'], ['24-35', 'adult'],
                   ['35-50', 'adult2'], ['50+', 'eldery']]
    elif update.callback_query.data in ['baby', 'toddler', 'kid', 'teen',
                                        'youth', 'adult', 'adult2', 'eldery']:
        search_keys.append(update.callback_query.data)
        img_path = "img/6.png"
        options = [['Так, студент', 'ucu'],
                   ['Звичайно, викладач', 'ucu'], ['Ні', 'ucu_no']]
    elif update.callback_query.data in ['ucu', 'ucu_no']:
        search_keys.append(update.callback_query.data)

        img_path = "img/7.png"
        options = getsurveyres(search_keys)

        # additional_button = True
        # add_option = ['На жаль, ні', 'add']
    # elif update.callback_query.data == 'add':
    #     img_path = "img/8.png"
    #     options = getsurveyres(search_keys)[3:].append(['Все ще ні', 'fail'])
    # elif update.callback_query.data == 'fail':
    #     img_path = "img/9.png"
    bot.sendPhoto(chat_id=update.callback_query.message.chat_id,
                  photo=open(img_path, 'rb'))
    NewMenu(bot, update.callback_query.message.chat_id, options,
            text='*тиць*')
    if additional_button:
        NewMenu(bot, update.callback_query.message.chat_id, add_options,
                text='*тиць*')


def gift_input(update, bot):
    gift = MessageHandler(Filters.text, get_name, pass_user_data=True)
    print(gift)

updater = Updater('771823969:AAFjzm1PYcY09N1gUvi3D9mKCPR0-3GXVdo')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button_press))
updater.dispatcher.add_handler(CommandHandler('gift', gift_input))

updater.start_polling()
updater.idle()
