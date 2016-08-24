#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Made by @SparkiL

from telegram import Bot
from telegram.ext import CommandHandler, Updater
import logging
import random

# Get the token from tokens file
import tokens
TOKEN = tokens.ABACAXI_TOKEN

open_pineapples = {}

# Constants
EMOJI_BOTH_HANDS = "\ud83d\ude4c"
EMOJI_CLOSED_HAND = "\ud83d\udc4a"
EMOJI_HAND = "\ud83d\udd90"
EMOJI_FINGER = "\u261d\ufe0f"
EMOJI_TWO_FINGER = "\u270c"
EMOJI_PINEAPPLE = "\ud83c\udf4d"
EMOJI_SADFACE = "\ud83d\ude22"

EMOJI_EXPRESSIONLESS = "\ud83d\ude11"
EMOJI_UNAMUSED = "\ud83d\ude12"
EMOJI_THINKING = "\ud83e\udd14"
IGNORE_EMOJIS = [EMOJI_UNAMUSED, EMOJI_EXPRESSIONLESS, EMOJI_THINKING]

MESSAGE_ALREADY_OPEN = "Já tem um abacaxi aberto:\n{0}"
MESSAGE_WHO_IGNORED = "Quem ignorou:"
MESSAGE_WHO_WANTS = EMOJI_CLOSED_HAND + " Quem quer <b>{0}</b>:"
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
def send_message(bot, chat_id, text, parse_mode='HTML'):
    bot.send_message(chat_id, text, parse_mode=parse_mode)


def fingers_and_name(name, fingers):
    if fingers >= 10:
        return EMOJI_BOTH_HANDS + " " + name
    elif fingers >= 5:
        return EMOJI_HAND + " " + name
    elif fingers >= 2:
        return EMOJI_TWO_FINGER + " " + name
    elif fingers <= 0:
        return IGNORE_EMOJIS[-fingers] + " " + name
    else:
        return EMOJI_FINGER + " " + name


def get_fingers_list(adopters_dict):
    message = ""
    for adopter, fingers in adopters_dict.items():
        if fingers > 0:
            message += "\n" + fingers_and_name(adopter, fingers)
    return message


def get_ignores_list(adopters_dict):
    message = ""
    for adopter, fingers in adopters_dict.items():
        if fingers <= 0:
            message += "\n" + fingers_and_name(adopter, fingers)
    return message


def get_full_list(adopters_dict):
    return get_fingers_list(adopters_dict) + get_ignores_list(adopters_dict)


# Pineapple manipulation
def open_pineapple(chat_id, action):
    logger.info("Pineapple action: %s" % action)
    open_pineapples[chat_id] = {'action': action, 'adopters': {}}
    return MESSAGE_NEW_PINEAPPLE.format(action)


def finger(chat_id, user):
    name = user.first_name + " " + user.last_name

    if open_pineapples[chat_id]['adopters'].setdefault(name, 0) >= 10:
        return MESSAGE_NO_MORE_FINGERS_IN_HAND

    open_pineapples[chat_id]['adopters'][name] += 1
    return get_full_list(open_pineapples[chat_id]['adopters'])


def ignore(chat_id, user):
    name = user.first_name + " " + user.last_name
    value = random.randint(-(len(IGNORE_EMOJIS)-1), 0)
    open_pineapples[chat_id]['adopters'][name] = value
    return get_full_list(open_pineapples[chat_id]['adopters'])


def close_pineapple(chat_id):
    pineapple = open_pineapples.pop(chat_id)
    if len(pineapple['adopters']) == 0:
        return MESSAGE_NO_ONE.format(pineapple['action'])

    fingers_list = get_fingers_list(pineapple['adopters'])
    ignores_list = get_ignores_list(pineapple['adopters'])

    message = ""
    if fingers_list != "":
        message += MESSAGE_WHO_WANTS.format(pineapple['action'])
        message += fingers_list

    if ignores_list != "":
        message += "\n" + MESSAGE_WHO_IGNORED
        message += ignores_list

    return message


# Commands
def open_pineapple_command(bot, update, args):
    chat_id = update.message.chat_id
    logger.info("Opening pineapple on %s" % chat_id)
    if len(args) == 0:
        logger.info("Not enough arguments")
        send_message(bot, chat_id, MESSAGE_USAGE_OPEN, None)
        return
    if chat_id in open_pineapples.keys():
        logger.info("Pineapple already open")
        send_message(bot, chat_id, MESSAGE_ALREADY_OPEN.format(
            MESSAGE_NEW_PINEAPPLE.format(open_pineapples[chat_id]['action'])))
        return
    message = open_pineapple(chat_id, ' '.join(args))
    send_message(bot, chat_id, message)


def finger_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Finger on %s" % chat_id)
    if chat_id not in open_pineapples.keys():
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE_NOT_YET_OPEN)
        return
    message = finger(chat_id, update.message.from_user)
    send_message(bot, chat_id, message)


def who_finger_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Getting fingers on %s" % chat_id)
    if chat_id not in open_pineapples.keys():
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE_NOT_YET_OPEN)
        return
    message = get_fingers_list(open_pineapples[chat_id]['adopters'])
    send_message(bot, chat_id, message)


def ignore_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Getting fingers on %s" % chat_id)
    if chat_id not in open_pineapples.keys():
        logger.info("Pineapple not open")
        send_message(bot, chat_id, MESSAGE_NOT_YET_OPEN)
        return
    message = ignore(chat_id, update.message.from_user)
    send_message(bot, chat_id, message)


def close_pineapple_command(bot, update):
    chat_id = update.message.chat_id
    logger.info("Close pineapple on %s" % chat_id)
    if chat_id not in open_pineapples.keys():
        logger.info("Pineapple already closed")
        send_message(bot, chat_id, MESSAGE_NOT_YET_OPEN)
        return
    message = close_pineapple(chat_id)
    send_message(bot, chat_id, message)


def main():
    random.seed()

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('abacaxi', open_pineapple_command, pass_args=True))
    dp.add_handler(CommandHandler('dedo', finger_command))
    dp.add_handler(CommandHandler('dedodequem', who_finger_command))
    dp.add_handler(CommandHandler('ignorar', ignore_command))
    dp.add_handler(CommandHandler('fechar', close_pineapple_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
