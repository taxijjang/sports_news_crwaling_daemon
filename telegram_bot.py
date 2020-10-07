from datetime import date, time, datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler

import requests

BOT_TOKEN = '531768435:AAHaf3-O5zKttSKKSdyB1OBd_TYCF9NwIOI'

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

FLATFORM, CATEGORY, NEWS = range(3)

base_url = 'http://127.0.0.1:5000/'


def flat_form_buttons(update, context):
    '''
    현재 볼 수 있는 플랫폼을 나타낸다

    TODO:: 지금은 2개 밖에 없어서 하드코딩으로 해놨는데 나중에 많아지면 동적으로 할수 있게 할 예정
    '''
    chat_id = update.message.chat_id
    task_buttons = [[
        InlineKeyboardButton('1.네이버 뉴스', callback_data='naver')
        , InlineKeyboardButton('2.다음 뉴스', callback_data='daum')
    ]]

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=chat_id
        , text='보시고 싶은 플랫폼을 골라주세요'
        , reply_markup=reply_markup
    )

    start_keyboard = [['/start']]
    start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id
        , text='처음부터 보시려면 키보드 화면에 있는 /start를 눌러주세요'
        , reply_markup=start_markup
    )

    return CATEGORY


def categpry_button(update, context):
    '''
    해당 플랫폼이 제공하는 뉴스 카테고리를 나타낸다.
    '''

    query = update.callback_query
    chat_id = query.message.chat_id
    flat_form = query.data

    url = f'{base_url}/flat_form_list/{flat_form}'
    response = requests.get(url)
    response_json = response.json()

    categories = response_json['message']

    task_buttons = list()

    for index, category in enumerate(categories):
        category_btn = list()
        category_btn.append(InlineKeyboardButton(f'{index + 1}. {category}', callback_data=f'{flat_form}/{category}'))
        task_buttons.append(category_btn)

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=chat_id,
        text='보시고 싶은 카테고리를 골라주세요',
        reply_markup=reply_markup
    )

    return NEWS


def news_list(update, context):
    '''
    해당 플랫폼, 카테고리에서 제공하는 뉴스를 순위대로 나타내 준다
    '''
    query = update.callback_query
    chat_id = query.message.chat_id
    flat_form_category = query.data

    url = f'{base_url}/{flat_form_category}'
    response = requests.get(url)
    response_json = response.json()

    news = response_json['message']

    ans = f'{str(datetime.now())} \n\n'
    for rank in range(len(news)):
        ans += f'{rank + 1}위 : {news[str(rank + 1)]["title"]} \n url : {news[str(rank + 1)]["url"]} \n\n'
    context.bot.send_message(chat_id=chat_id, text=ans)

def not_found(update, context):
    '''
    서버의 연결이 원활하지 않을때
    '''
    chat_id = update.message.chat_id

    ans = "서버의 연결이 원활하지 않습니다"
    context.bot.send_message(chat_id=chat_id,text=ans)

    start_keyboard = [['/start']]
    start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id
        , text='처음부터 보시려면 키보드 화면에 있는 /start를 눌러주세요'
        , reply_markup=start_markup
    )


if __name__ == '__main__':
    '''
    TODO:: 추후에 예외 처리를 좀 해줘야한다.
           예를들면 서버와의 연결이 되지 않을때 등등.....
    '''
    test_conv_hanlder = ConversationHandler(
        entry_points=[CommandHandler('start', flat_form_buttons, pass_args=True)],
        states={
            FLATFORM: [CallbackQueryHandler(flat_form_buttons)],
            CATEGORY: [CallbackQueryHandler(categpry_button)],
            NEWS: [CallbackQueryHandler(news_list)]
        },
        fallbacks=[CommandHandler('start', flat_form_buttons, pass_args=True)],
        allow_reentry=True
    )

    updater.dispatcher.add_handler(test_conv_hanlder)

    updater.start_polling()
    updater.idle()
