#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Made by @SparkiL

from telegram.ext import CommandHandler, Updater
import logging

from classes.constants import MESSAGE
from classes.pineapple import Pineapple, Finger


# Get the token from tokens file
import tokens
TOKEN = tokens.ABACAXI_TOKEN


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# Utils
def get_full_name(user):
    return user.first_name + " " + user.last_name


def send_message(bot, chat_id, text, parse_mode='HTML'):
    bot.send_message(chat_id, text, parse_mode=parse_mode)


# Commands
def open_pineapple_command(bot, update, args):
    chat_id = update.message.chat_id
    logger.info("Opening pineapple on %s" % chat_id)

    if len(args) == 0:
        logger.info("Not enough arguments")
        send_message(bot, chat_id, MESSAGE.USAGE_OPEN, None)
        return

    if Pineapple.is_open(chat_id):
        logger.info("Pineapple already open")
        send_message(bot, chat_id, MESSAGE.ALREADY_OPEN.format(
            Pineapple.get(chat_id).get_open_message()))
        return

    owner_name = get_full_name(update.message.from_user)
    Pineapple.open(chat_id, ' '.join(args), owner_name)
    message = Pineapple.get(chat_id).get_open_message()
    send_message(bot, chat_id, message)


def finger_in_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Finger on %s" % chat_id)

    if not Pineapple.is_open(chat_id):
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE.NOT_YET_OPEN)
        return

    user_name = get_full_name(update.message.from_user)
    pineapple = Pineapple.get(chat_id)
    try:
        pineapple.finger_in(user_name)
        message = pineapple.get_short_fingers_list_message()
    except Finger.FingersLimitReached:
        message = MESSAGE.NO_MORE_FINGERS_IN_HAND

    send_message(bot, chat_id, message)


def who_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Getting fingers on %s" % chat_id)

    if not Pineapple.is_open(chat_id):
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE.NOT_YET_OPEN)
        return

    message = Pineapple.get(chat_id).get_fingers_list_message()
    send_message(bot, chat_id, message)


def finger_out_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Getting fingers on %s" % chat_id)

    if not Pineapple.is_open(chat_id):
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE.NOT_YET_OPEN)
        return

    user_name = get_full_name(update.message.from_user)
    pineapple = Pineapple.get(chat_id)
    pineapple.finger_out(user_name)

    message = pineapple.get_short_fingers_list_message()
    send_message(bot, chat_id, message)


def close_pineapple_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Close pineapple on %s" % chat_id)

    if not Pineapple.is_open(chat_id):
        logger.info("Pineapple already closed")
        send_message(bot, chat_id, MESSAGE.NOT_YET_OPEN)
        return

    message = Pineapple.get(chat_id).get_close_message()
    Pineapple.close(chat_id)
    send_message(bot, chat_id, message)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('abacaxi', open_pineapple_command, pass_args=True))
    dp.add_handler(CommandHandler('dedo', finger_in_command))
    dp.add_handler(CommandHandler('quem', who_command))
    dp.add_handler(CommandHandler('dedofora', finger_out_command))
    dp.add_handler(CommandHandler('fechar', close_pineapple_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
