#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import re
from datetime import datetime
from io import BytesIO
from typing import List

import time

import sys

from PIL import Image
from django_telegrambot.apps import DjangoTelegramBot
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Message
from telegram import MessageEntity
from telegram import ReplyKeyboardMarkup, KeyboardButton, Contact
from telegram.ext import CallbackQueryHandler
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

from Charity.models import HelperProfile, Project, ManyToMany, HelpType, Case, Institute
from django.contrib.auth.models import User

from bot import util
from bot.models import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, USER_PASSWORD, USER_NAME, CONTACT_RESPONSE, SEND_REPORT, DO_HELP, SEARCH_RESULT, HELP_TYPE_CALLBACK, PROJECT_CALLBACK = range(
    9)

reply_keyboard = [['درباره حاتم📽', 'دعوت دوستان👬'],
                  ['گزارش📢', 'ثبت نام✍🏼'],
                  ['انجام کمک🤝']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

return_keyboard = [['بازگشت به منوی اصلی🔄', 'مرحله قبل🔙']]
return_markup = ReplyKeyboardMarkup(return_keyboard, one_time_keyboard=True)

phone_keyboard = [[KeyboardButton(text='ارسال شماره تماس', request_contact=True, request_location=False)],
                  ['بازگشت به منوی اصلی🔄', 'مرحله قبل🔙']]
phone_markup = ReplyKeyboardMarkup(phone_keyboard, one_time_keyboard=True)

help_keyboard = [['جستجو بر اساس کلمه کلیدی🔍', 'مشاهده بر اساس دسته بندی🗞'],
                 ['بازگشت به منوی اصلی🔄', 'مرحله قبل🔙']]

help_markup = ReplyKeyboardMarkup(help_keyboard)


class BotUser:
    def __init__(self):
        self.contact = None
        self.username = None
        self.password = None
        self.projects = None
        self.last_message = None


bot_user = BotUser()


def start(bot, update):
    update.message.reply_text(
        "با حاتم کارهای خیرخواهانه خود را مدیریت و برنامه ریزی کنید",
        reply_markup=markup)
    bot_user.last_action = CHOOSING
    return CHOOSING


def about_hatam(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text('💐💐💐💐💐💐💐💐💐💐💐'
                              '\nحاتم یک پلتفرم و سامانه ی هوشمند برای برقراری ارتباطی مؤثر تر بین خیرین و داوطلبان با موسسات مردم نهاد است که به صورت حمایت و فعالیت داوطلبانه در سه زمینه ی مالی، خدمات و کالایی در پروژه های تعریف شده از سوی موسسه ها صورت می گیرد.'
                              'حاتم توسط جمعی از دانشجویان دانشگاه صنعتی شریف با حمایت کامل دانشگاه شکل گرفته است، مشاهدات و تجربیات ما گواه بر این بود که در زمینه های گوناگونی می توان در کمک و توانمندسازی مددجویان کار و فعالیت کرد و با اینکه موسسات زیادی در زمینه های گوناگونی مثل کودک کار، اتیسم، محیط زیست و… در حال فعالیت هستند حلقه ای مفقوده بین موسسات و داوطلبین مشاهده می شد، گویا در پیدا کردن هم مشکلی وجود دارند، پتانسیل هایی که دارند به علل مختلف از دست می روند، همگی در اطرافمان افراد زیادی را که هریک تخصصی دارند می بینیم که علاقه به فعالیت های بشر دوستانه دارند اما به علت مشغله و اینکه پیدا کردن پروژه و کار خیرخواهانه ای که با تخصص و شرایط زمانی شخص همسو باشد کاری دشوار است و با قرار گرفتن در روزمره گی تقریبا به کاری بسیار غیر ممکن تبدیل می شود از سویی هم مؤسسات برای معرفی و شناساندن خود به عموم با محدودیت هایی همچون بودجه و کانال های ارتباطی رو به رو هستند، هدف اصلی از تشکیل حاتم پرکردن جای آن حلقه مفقوده است.'
                              'هدف از ایجاد حاتم بهره وری از افراد متخصص و افزایش فعالیت داوطلبانه و حمایتی برای اهداف بشردوستانه است که در کنار کمک به مددجویان در جلا بخشیدن به روح و قلب داوطلب تأثیر شایانی دارد و مؤسسات می توانند با فعالیت در بستر حاتم خود را تقویت کنند و به اهدافشان نزدیک تر شوند، اهدافی که در منشور اهداف حاتم ذکر شده است و تمامی مؤسسات حاظر در سامانه آن را قبول دارند.\n'
                              '🌷🌷🌷🌷🌷🌷🌷🌷🌷🌷🌷', reply_markup=markup)
    bot_user.last_action = CHOOSING

    return CHOOSING


def invite_friends(bot, update):
    update.message.reply_text(
        'با ارسال پیام زیر به دوستان خود در ترویج فرهنگ مهروزی در ایران اسلامی عزیزمان کمک نمایید\n\n👇👇👇👇👇👇👇👇',
        reply_markup=markup)
    bot.sendPhoto(chat_id=update.message.chat_id, photo='AgADBAADd6kxG-oYkFCsvLASB_1qldDmnxkABGzNTfGtxvNqNQkEAAEC',
                  caption='\nافراد نیازمندی هستند که تنها مهارت تو هست که میتونه نیازشون رو رفع کنه\n\nخوشحال میشیم که تو رو تو جمع خودمون ببینیم\n👇👇👇👇👇👇👇👇\n\n'
                          'http://t.me/hatam_system_bot')

    bot_user.last_action = CHOOSING

    return CHOOSING


def register(bot, update):
    update.message.reply_text('برای ثبت نام لازم است تا شماره شما را در سامانه داشته باشیم\n'
                              'لطفا برای ادامه فرایند ثبت نام بر روی کلید زیر کلیک نمایید.', reply_markup=phone_markup)
    return CONTACT_RESPONSE


def get_user_contact(bot, update):
    contact = update.message.contact
    bot_user.contact = contact
    update.message.reply_text('لطفا یک نام کاربری به زبان انگلیسی برای خود انتخاب نمایید\n'
                              'سعی کنید نام کاربری به گونه ای باشد که آن را در ذهن به خاطر داشته باشید',
                              reply_markup=return_markup)

    return USER_NAME


def get_user_name(bot, update):
    user_name = update.message.text
    if re.match("^[a-zA-Z0-9_.-]+$", user_name):
        if User.objects.filter(username=user_name).exists():
            update.message.reply_text('این نام کاربری توسط شخصی دیگر قبلا انتخاب شده است\n'
                                      'لطفا یک نام کاربری دیگر انتخاب نمایید.', reply_markup=return_markup)
            return USER_NAME
        else:
            bot_user.username = user_name
            update.message.reply_text('لطفا یک رمز عبور برای خود انتخاب نمایید.\n'
                                      'رمز عبور بایستی حداقل شامل ۸ حرف به همراه عدد باشد', reply_markup=return_markup)
            return USER_PASSWORD
    else:
        update.message.reply_text('نام کاربری باید تنها شامل حروف انگلیسی و اعداد به همراه [.-_] باشد',
                                  reply_markup=return_markup)
        return USER_NAME


def get_user_password(bot, update):
    user_password = update.message.text
    if re.match(r'^(?=.*?\d)(?=.*?[a-z])[A-Za-z@\-\d]{8,}$', user_password):
        bot_user.password = user_password
        user = User.objects.create_user(username=bot_user.username, password=user_password)
        user.save()
        update.message.reply_text('ثبت نام شما با موفقیت انجام شد')
    else:
        update.message.reply_text('رمز عبور ضعیف است دوباره وارد کنید', reply_markup=return_markup)
        return USER_PASSWORD


def send_report(bot, update):
    update.message.reply_text('لطفا گزارش خود را نوشته و آن را ارسال نمایید\n', reply_markup=return_markup)
    return SEND_REPORT


def get_user_report(bot, update):
    user_chat_id = update.message.chat.id
    text = update.message.text
    report = Reports.objects.create(chat_id=user_chat_id, text=text)
    report.save()
    update.message.reply_text('گزارش شما دریافت شد\n'
                              'ممنون بابت ارسال گزارش', reply_markup=return_markup)


def do_help(bot, update):
    update.message.reply_text('برای مشاهده پروژه های کمک رسانی یکی از دو روش زیر را انتخاب نمایید',
                              reply_markup=help_markup)
    return DO_HELP


def get_project_by_groups(bot, update):
    root_helps = HelpType.objects.filter(father=None)
    button_list = list()
    for root_help in root_helps:
        button_list.append(InlineKeyboardButton(text=root_help.title, callback_data=root_help.title))
    reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
    update.message.reply_text('لطفا یکی از دسته های زیر را انتخاب نمایید', reply_markup=reply_markup)
    bot_user.old_message = update.message
    bot_user.old_reply_markup = reply_markup
    return HELP_TYPE_CALLBACK


def help_type_callback(bot, update):
    query = update.callback_query
    root_help = HelpType.objects.filter(title=query.data).first()
    child_helps = HelpType.objects.filter(father=root_help)

    button_list = list()
    if child_helps.count() > 0:
        for child_help in child_helps:
            button_list.append(InlineKeyboardButton(text=child_help.title, callback_data=child_help.title))
        reply_markup = InlineKeyboardMarkup(
            util.build_menu(button_list, n_cols=1))
        bot_user.old_reply_markup = reply_markup
        bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                      text='لطفا یکی از دسته های زیر را انتخاب نمایید',
                                      reply_markup=reply_markup)
        return HELP_TYPE_CALLBACK
    else:
        projects_button_list = list()
        header_button_list = [
            InlineKeyboardButton(text='بعدی◀', callback_data='1,1')]
        all_projects = Project.objects.filter(help_type=root_help, institute__accepted=True)
        bot_user.projects = all_projects
        if all_projects.count() > 0:
            min_projects = min(5, len(all_projects))
            for i in range(0, min_projects):
                projects_button_list.append(InlineKeyboardButton(text=all_projects[i].title,
                                                                 callback_data='0,' + all_projects[i].title))
            if len(all_projects) > 5:
                reply_markup = InlineKeyboardMarkup(
                    util.build_menu(projects_button_list, n_cols=1, header_buttons=header_button_list))
            else:
                reply_markup = InlineKeyboardMarkup(util.build_menu(projects_button_list, n_cols=1))

            bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                          reply_markup=reply_markup)
            bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                  text='لطفا یکی از پروژه های زیر را انتخاب نمایید', reply_markup=reply_markup)
            return PROJECT_CALLBACK
        else:
            bot.sendMessage(chat_id=query.message.chat_id, text='در حال حاظر پروژه ای در بخش وجود ندارد', )


def project_callback(bot, update):
    query = update.callback_query
    query_data = query.data.split(',')
    projects_button_list = list()
    all_projects = bot_user.projects
    if query_data[0] is '1':
        index = int(query_data[1]) * 5
        next = int(query_data[1]) + 1
        previous = int(query_data[1]) - 1
        header_button_list = None
        footer_button_list = None
        min_projects = min(index + 5, len(all_projects))
        for index in range(index, min_projects):
            projects_button_list.append(InlineKeyboardButton(text=all_projects[index].title,
                                                             callback_data='0,' + all_projects[index].title))
        if len(all_projects) > (index + 5):
            header_button_list = [InlineKeyboardButton(text='بعدی◀', callback_data='1,' + str(next))]
        if previous != -1:
            footer_button_list = [InlineKeyboardButton(text='▶قبلی', callback_data='1,' + str(previous))]
        reply_markup = InlineKeyboardMarkup(
            util.build_menu(projects_button_list, n_cols=1,
                            header_buttons=header_button_list, footer_buttons=footer_button_list))
        bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                      reply_markup=reply_markup)
        bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
                              text='لطفا یکی از پروژه های زیر را انتخاب نمایید', reply_markup=reply_markup)
        return PROJECT_CALLBACK

    else:
        selected_project = Project.objects.filter(title=query_data[1]).first()
        link_url = '127.0.0.1:9090/charity/project/' + str(selected_project.id)
        if bot_user.last_message is None:
            mess = bot.sendMessage(chat_id=query.message.chat_id, text='لینک پروژه : ' + link_url + '\n' +
                                                                       'عنوان پروژه :' + selected_project.title + '\n' +
                                                                       'نام موسسه : ' + selected_project.institute.title + '\n' +
                                                                       'تاریخ شروع پروژه : ' + selected_project.start_date.strftime(
                '%d/%m/%Y') + '\n' +
                                                                       'تاریخ پایان پروژه : ' + selected_project.end_date.strftime(
                '%d/%m/%Y') + '\n' +
                                                                       'رده سنی مورد نیاز : ' + str(
                selected_project.min_age) + ' الی ' + str(selected_project.max_age) + 'سال\n' +
                                                                       'پروژه در یک جمله : ' + selected_project.sentence + '\n' +
                                                                       'جنسیت مورد نیاز : ' + str(
                selected_project.get_gender_display()) + '\n' +
                                                                       'گروه مخاطب پروژه : ' + str(
                selected_project.get_addressed_display()) + '\n')
        else:
            mess = bot.edit_message_text(chat_id=query.message.chat_id, message_id=bot_user.last_message.message_id,
                                         text='لینک پروژه : ' + link_url + '\n' +
                                              'عنوان پروژه :' + selected_project.title + '\n' +
                                              'نام موسسه : ' + selected_project.institute.title + '\n' +
                                              'تاریخ شروع پروژه : ' + selected_project.start_date.strftime(
                                             '%d/%m/%Y') + '\n' +
                                              'تاریخ پایان پروژه : ' + selected_project.end_date.strftime(
                                             '%d/%m/%Y') + '\n' +
                                              'رده سنی مورد نیاز : ' + str(
                                             selected_project.min_age) + ' الی ' + str(
                                             selected_project.max_age) + 'سال\n' +
                                              'پروژه در یک جمله : ' + selected_project.sentence + '\n' +
                                              'جنسیت مورد نیاز : ' + str(
                                             selected_project.get_gender_display()) + '\n' +
                                              'گروه مخاطب پروژه : ' + str(
                                             selected_project.get_addressed_display()) + '\n')
            # bot_user.last_message = mess


def get_project_by_search(bot, update):
    update.message.reply_text('لطفا عنوان جستجوی خود را در یک کلمه نوشته و ارسال نمایید\n',
                              reply_markup=return_markup)
    return SEARCH_RESULT


def search_result(bot, update):
    projects_button_list = list()
    searched_projects = Project.objects.filter(title__contains=update.message.text)
    if searched_projects.count() > 0:
        for p in searched_projects:
            projects_button_list.append(InlineKeyboardButton(text=p.title, callback_data='0,' + p.title))
        reply_markup = InlineKeyboardMarkup(util.build_menu(projects_button_list, n_cols=1))
        bot.sendMessage(chat_id=update.message.chat_id, text='لطفا یکی از پروژه های زیر را انتخاب نمایید',
                        reply_markup=reply_markup)
        return PROJECT_CALLBACK
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='نتیجه ای یافت نشد!', )


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def restart(bot, update):
    bot.send_message(update.message.chat_id, "Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


def main():
    # Create the Updater and pass it your bot's token.
    # updater = Updater("395171287:AAHpcFfqbIZZNK209cnUglaM8h0N4fK69J4")
    # Get the dispatcher to register handlers
    dp = DjangoTelegramBot.dispatcher
    # dp = DjangoTelegramBot.getDispatcher('395171287:AAHpcFfqbIZZNK209cnUglaM8h0N4fK69J4')
    # dp.add_handler(CommandHandler("start", start))
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^درباره حاتم📽$',
                                    about_hatam,
                                    pass_user_data=True),
                       RegexHandler('^دعوت دوستان👬$',
                                    invite_friends),
                       RegexHandler('ثبت نام✍🏼$', register),
                       RegexHandler('گزارش📢$', send_report),
                       RegexHandler('انجام کمک🤝$', do_help),
                       ],

            CONTACT_RESPONSE: [MessageHandler(Filters.contact, get_user_contact),
                               RegexHandler('بازگشت به منوی اصلی🔄$', start),
                               RegexHandler('مرحله قبل🔙$', start)],
            USER_NAME: [RegexHandler('بازگشت به منوی اصلی🔄$', start),
                        RegexHandler('مرحله قبل🔙$', register),
                        MessageHandler(Filters.text, get_user_name)],

            USER_PASSWORD: [RegexHandler('بازگشت به منوی اصلی🔄$', start),
                            RegexHandler('مرحله قبل🔙$', register),
                            MessageHandler(Filters.text, get_user_password)],

            SEND_REPORT: [RegexHandler('بازگشت به منوی اصلی🔄$', start),
                          RegexHandler('مرحله قبل🔙$', start),
                          MessageHandler(Filters.text, get_user_report)],

            DO_HELP: [RegexHandler('جستجو بر اساس کلمه کلیدی🔍$', get_project_by_search),
                      RegexHandler('مشاهده بر اساس دسته بندی🗞$', get_project_by_groups),
                      RegexHandler('بازگشت به منوی اصلی🔄$', start),
                      RegexHandler('مرحله قبل🔙$', start)],

            SEARCH_RESULT: [RegexHandler('بازگشت به منوی اصلی🔄$', start),
                            RegexHandler('مرحله قبل🔙$', do_help),
                            MessageHandler(Filters.text, search_result)],

            HELP_TYPE_CALLBACK: [CallbackQueryHandler(help_type_callback),
                                 RegexHandler('جستجو بر اساس کلمه کلیدی🔍$', get_project_by_search),
                                 RegexHandler('مشاهده بر اساس دسته بندی🗞$', get_project_by_groups),
                                 RegexHandler('بازگشت به منوی اصلی🔄$', start),
                                 RegexHandler('مرحله قبل🔙$', start)],

            PROJECT_CALLBACK: [CallbackQueryHandler(project_callback),
                               RegexHandler('جستجو بر اساس کلمه کلیدی🔍$', get_project_by_search),
                               RegexHandler('مشاهده بر اساس دسته بندی🗞$', get_project_by_groups),
                               RegexHandler('بازگشت به منوی اصلی🔄$', start),
                               RegexHandler('مرحله قبل🔙$', start)]

        },

        fallbacks=[RegexHandler('^Done$', start, pass_user_data=True)]
    )
    #
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # dp.add_handler(CommandHandler('r', restart))

    # Start the Bot
    # updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()

    #
    # if __name__ == '__main__':
    #     main()
