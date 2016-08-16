#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Made by @SparkiL

from telegram import Bot
from telegram.ext import CommandHandler, Updater

# Create the bot
import tokens
TOKEN = tokens.ABACAXI_TOKEN
bot = Bot(TOKEN)

open_pineapples = {}

# Constants
EMOJI_HAND = "\ud83d\udc4a"
EMOJI_FINGER = "\u261d\ufe0f"
EMOJI_PINEAPPLE = "\ud83c\udf4d"
EMOJI_SADFACE = "\ud83d\ude22"

MESSAGE_ALREADY_OPEN = "Já tem um abacaxi aberto:\n{0}"
MESSAGE_CLOSE_PINEAPPLE = EMOJI_HAND + " Pessoas que querem <b>{0}</b>:"
MESSAGE_FINGER = EMOJI_FINGER
MESSAGE_NOT_YET_OPEN = "Nenhum abacaxi aberto."
MESSAGE_NO_ONE = "Ninguém quer <b>{0}</b>. " + EMOJI_SADFACE
MESSAGE_NEW_PINEAPPLE = "Quem quer <b>{0}</b> põe o dedo aqui,\nque já vai fechar\no abacaxi. " + EMOJI_PINEAPPLE
MESSAGE_USAGE_OPEN = "Uso:\n/abacaxi <ação>"


# Messaging
def send_message(chat_id, text, parse_mode='HTML'):
    bot.send_message(chat_id, text, parse_mode=parse_mode)


# Pineapple manipulation
def open_pineapple(chat_id, action):
    open_pineapples[chat_id] = {'action': action, 'adopters': []}
    send_message(chat_id, MESSAGE_NEW_PINEAPPLE.format(action))


def finger(chat_id, user):
    nick = user.username
    if nick is None or nick == "":
        nick = user.first_name

    if nick not in open_pineapples[chat_id]['adopters']:
        open_pineapples[chat_id]['adopters'].append(nick)
    send_message(chat_id, MESSAGE_FINGER)


def close_pineapple(chat_id):
    pineapple = open_pineapples.pop(chat_id)
    if len(pineapple['adopters']) == 0:
        send_message(chat_id, MESSAGE_NO_ONE.format(pineapple['action']))
        return

    message = MESSAGE_CLOSE_PINEAPPLE.format(pineapple['action'])
    for adopter in pineapple['adopters']:
        message += "\n" + EMOJI_FINGER + " " + adopter
    send_message(chat_id, message)


# Commands
def open_pineapple_command(bot, update, args):
    chat_id = update.message.chat_id
    if len(args) == 0:
        send_message(chat_id, MESSAGE_USAGE_OPEN, None)
        return
    if chat_id in open_pineapples.keys():
        send_message(chat_id, MESSAGE_ALREADY_OPEN.format(
            MESSAGE_NEW_PINEAPPLE.format(open_pineapples[chat_id]['action'])))
        return
    open_pineapple(chat_id, ' '.join(args))


def finger_command(bot, update):
    chat_id = update.message.chat_id
    if chat_id not in open_pineapples.keys():
        send_message(chat_id, MESSAGE_NOT_YET_OPEN)
        return
    finger(chat_id, update.message.from_user)


def close_pineapple_command(bot, update):
    chat_id = update.message.chat_id
    if chat_id not in open_pineapples.keys():
        send_message(chat_id, MESSAGE_NOT_YET_OPEN)
        return
    close_pineapple(chat_id)


def main():
    updater = Updater(bot=bot)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('abacaxi', open_pineapple_command, pass_args=True))
    dp.add_handler(CommandHandler('dedo', finger_command))
    dp.add_handler(CommandHandler('fechar', close_pineapple_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
