#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Made by @SparkiL

from telegram import Bot
from telegram.ext import CommandHandler, Updater
import logging

# Create the bot
import tokens
TOKEN = tokens.ABACAXI_TOKEN
bot = Bot(TOKEN)

open_pineapples = {}

# Constants
EMOJI_BOTH_HANDS = "\ud83d\ude4c"
EMOJI_CLOSED_HAND = "\ud83d\udc4a"
EMOJI_HAND = "\ud83d\udd90"
EMOJI_FINGER = "\u261d\ufe0f"
EMOJI_TWO_FINGER = "\u270c"
EMOJI_PINEAPPLE = "\ud83c\udf4d"
EMOJI_SADFACE = "\ud83d\ude22"

MESSAGE_ALREADY_OPEN = "Já tem um abacaxi aberto:\n{0}"
MESSAGE_CLOSE_PINEAPPLE = EMOJI_CLOSED_HAND + " Quem quer <b>{0}</b>:"
MESSAGE_FINGER = EMOJI_FINGER
MESSAGE_NOT_YET_OPEN = "Nenhum abacaxi aberto."
MESSAGE_NO_MORE_FINGERS_IN_HAND = "Você não tem mais dedos em suas mãos."
MESSAGE_NO_ONE = "Ninguém quer <b>{0}</b>. " + EMOJI_SADFACE
MESSAGE_NEW_PINEAPPLE = "Quem quer <b>{0}</b>\npõe o dedo aqui,\nque já vai fechar\no abacaxi. " + EMOJI_PINEAPPLE
MESSAGE_USAGE_OPEN = "Uso:\n/abacaxi <ação>"


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# Messaging
def send_message(chat_id, text, parse_mode='HTML'):
    bot.send_message(chat_id, text, parse_mode=parse_mode)


def fingers_and_name(name, fingers):
    if fingers >= 10:
        return EMOJI_BOTH_HANDS + " " + name
    elif fingers >= 5:
        return EMOJI_HAND + " " + name
    elif fingers >= 2:
        return EMOJI_TWO_FINGER + " " + name
    else:
        return EMOJI_FINGER + " " + name


def get_fingers_list(adopters_dict):
    message = ""
    for adopter, fingers in adopters_dict.items():
        message += "\n" + fingers_and_name(adopter, fingers)
    return message


# Pineapple manipulation
def open_pineapple(chat_id, action):
    logger.info("Pineapple action: %s" % action)
    open_pineapples[chat_id] = {'action': action, 'adopters': {}}
    send_message(chat_id, MESSAGE_NEW_PINEAPPLE.format(action))


def finger(chat_id, user):
    name = user.first_name + " " + user.last_name

    if open_pineapples[chat_id]['adopters'].setdefault(name, 0) >= 10:
        send_message(chat_id, MESSAGE_NO_MORE_FINGERS_IN_HAND)
        return

    open_pineapples[chat_id]['adopters'][name] += 1
    send_message(chat_id, get_fingers_list(open_pineapples[chat_id]['adopters']))


def close_pineapple(chat_id):
    pineapple = open_pineapples.pop(chat_id)
    if len(pineapple['adopters']) == 0:
        send_message(chat_id, MESSAGE_NO_ONE.format(pineapple['action']))
        return

    message = MESSAGE_CLOSE_PINEAPPLE.format(pineapple['action'])
    message += get_fingers_list(pineapple['adopters'])
    send_message(chat_id, message)


# Commands
def open_pineapple_command(bot, update, args):
    chat_id = update.message.chat_id
    logger.info("Opening pineapple on %s" % chat_id)
    if len(args) == 0:
        logger.info("Not enough arguments")
        send_message(chat_id, MESSAGE_USAGE_OPEN, None)
        return
    if chat_id in open_pineapples.keys():
        logger.info("Pineapple already open")
        send_message(chat_id, MESSAGE_ALREADY_OPEN.format(
            MESSAGE_NEW_PINEAPPLE.format(open_pineapples[chat_id]['action'])))
        return
    open_pineapple(chat_id, ' '.join(args))


def finger_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Finger on %s" % chat_id)
    if chat_id not in open_pineapples.keys():
        logger.info("Pineapple not open")
        send_message(chat_id, MESSAGE_NOT_YET_OPEN)
        return
    finger(chat_id, update.message.from_user)


def who_finger_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Getting fingers on %s" % chat_id)
    if chat_id not in open_pineapples.keys():
        logger.info("Pineapple not open")
        send_message(chat_id, MESSAGE_NOT_YET_OPEN)
        return
    send_message(chat_id, get_fingers_list(open_pineapples[chat_id]['adopters']))


def close_pineapple_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Close pineapple on %s" % chat_id)
    if chat_id not in open_pineapples.keys():
        logger.info("Pineapple already closed")
        send_message(chat_id, MESSAGE_NOT_YET_OPEN)
        return
    close_pineapple(chat_id)


def main():
    updater = Updater(bot=bot)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('abacaxi', open_pineapple_command, pass_args=True))
    dp.add_handler(CommandHandler('dedo', finger_command))
    dp.add_handler(CommandHandler('dedodequem', who_finger_command))
    dp.add_handler(CommandHandler('fechar', close_pineapple_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
