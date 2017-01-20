#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Made by @SparkiL

from telegram import KeyboardButton, ReplyKeyboardHide, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import json
import os


# Change the working directory to the file's directory
abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

from classes.constants import EMOJI, MESSAGE
from classes.logger import logger
from classes.pineapple import Pineapple, Finger


# Get the token from environment variable
TOKEN = os.environ['TOKEN']


# Utils
def get_full_name(user):
    return user.first_name + " " + user.last_name


def send_message(
        bot,
        chat_id,
        text,
        parse_mode='Markdown',
        reply_markup=None,
        reply_to_message_id=None):
    bot.send_message(
        chat_id,
        text,
        parse_mode=parse_mode,
        reply_to_message_id=reply_to_message_id,
        reply_markup=reply_markup)


def create_pineapple_reply_keyboard():
    button_finger_in = KeyboardButton(EMOJI.FINGER)
    button_finger_out = KeyboardButton(EMOJI.FINGER_DOWN)
    keyboard = ReplyKeyboardMarkup([[button_finger_in], [button_finger_out]], one_time_keyboard=True)
    return keyboard


def text_equals_emoji(text, emoji):
    jtext = json.dumps(text)
    jemoji = json.dumps(emoji)
    return jtext == jemoji


# Commands
def help_command(bot, update):
    chat_id = update.message.chat_id
    send_message(bot, chat_id, MESSAGE.HELP)


def open_pineapple_command(bot, update, args):
    chat_id = update.message.chat_id
    logger.info("Opening pineapple on %s" % chat_id)

    if len(args) == 0:
        logger.info("Not enough arguments")
        send_message(bot, chat_id, MESSAGE.USAGE_OPEN)
        return

    if Pineapple.is_open(chat_id):
        logger.info("Pineapple already open")
        send_message(bot, chat_id, MESSAGE.ALREADY_OPEN.format(
            Pineapple.get(chat_id).get_open_message()))
        return

    owner_name = get_full_name(update.message.from_user)
    Pineapple.open(chat_id, ' '.join(args), owner_name)
    message = Pineapple.get(chat_id).get_open_message()
    keyboard = create_pineapple_reply_keyboard()
    send_message(bot, chat_id, message, reply_markup=keyboard)


def finger_in_command(bot, update, args, is_reply=False):
    chat_id = update.message.chat_id
    logger.info("Finger on %s" % chat_id)

    if not Pineapple.is_open(chat_id):
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE.NOT_YET_OPEN)
        return

    user_name = get_full_name(update.message.from_user)
    pineapple = Pineapple.get(chat_id)

    if len(args) == 2 and "".join(args) == "domeio":  # Easter Egg
        pineapple.middle_finger(user_name)
        message = pineapple.get_short_fingers_list_message()
    else:
        try:
            pineapple.finger_in(user_name)
            Pineapple.update(chat_id, pineapple)
            message = pineapple.get_short_fingers_list_message()
        except Finger.FingersLimitReached:
            message = MESSAGE.NO_MORE_FINGERS_IN_HAND

    if is_reply:
        message_id = update.message.message_id
    else:
        message_id = None
    send_message(bot, chat_id, message, reply_to_message_id=message_id, reply_markup=ReplyKeyboardHide(selective=True))


def who_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Getting fingers on %s" % chat_id)

    if not Pineapple.is_open(chat_id):
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE.NOT_YET_OPEN)
        return

    message = Pineapple.get(chat_id).get_fingers_list_message()
    send_message(bot, chat_id, message)


def finger_out_command(bot, update, is_reply=False):
    chat_id = update.message.chat_id
    logger.info("Getting fingers on %s" % chat_id)

    if not Pineapple.is_open(chat_id):
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE.NOT_YET_OPEN)
        return

    user_name = get_full_name(update.message.from_user)
    pineapple = Pineapple.get(chat_id)
    pineapple.finger_out(user_name)
    Pineapple.update(chat_id, pineapple)

    message = pineapple.get_short_fingers_list_message()

    if is_reply:
        message_id = update.message.message_id
    else:
        message_id = None
    send_message(bot, chat_id, message, reply_to_message_id=message_id, reply_markup=ReplyKeyboardHide(selective=True))


def close_pineapple_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Close pineapple on %s" % chat_id)

    if not Pineapple.is_open(chat_id):
        logger.info("Pineapple already closed")
        send_message(bot, chat_id, MESSAGE.NOT_YET_OPEN)
        return

    message = Pineapple.get(chat_id).get_close_message()
    Pineapple.close(chat_id)
    send_message(bot, chat_id, message, reply_markup=ReplyKeyboardHide())


def message_handler(bot, update):
    """Check if is a finger in or out"""
    text = update.message.text
    logger.info("Reply on %s: %s" % (str(update.message.chat_id), text.encode('utf-8')))
    if text_equals_emoji(text, EMOJI.FINGER):
        finger_in_command(bot, update, [], is_reply=True)
    elif text_equals_emoji(text, EMOJI.FINGER_DOWN):
        finger_out_command(bot, update, is_reply=True)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('abacaxi', open_pineapple_command, pass_args=True))
    dp.add_handler(CommandHandler('dedo', finger_in_command, pass_args=True))
    dp.add_handler(CommandHandler('quem', who_command))
    dp.add_handler(CommandHandler('dedofora', finger_out_command))
    dp.add_handler(CommandHandler('fechar', close_pineapple_command))
    dp.add_handler(MessageHandler([Filters.text], message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
