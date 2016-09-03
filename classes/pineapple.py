#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from .constants import EMOJI, MESSAGE

logger = logging.getLogger(__name__)


class Finger(object):
    def __init__(self):
        self.count = 1
        self.is_in = True
        self.update_emoji()

    class FingersLimitReached(Exception):
        def __init__(self, message=''):
            super(Finger.FingersLimitReached, self).__init__(message)

    def increment(self):
        self.is_in = True
        if self.count >= 10:
            raise Finger.FingersLimitReached()
        self.count += 1
        self.update_emoji()

    def set_out(self):
        self.is_in = False
        self.count = 0
        self.update_emoji()

    def update_emoji(self):
        if self.is_in:
            self.set_emoji_from_finger_count()
        else:
            self.set_emoji_from_random_out()

    def set_emoji_from_finger_count(self):
        if self.count < 2:
            self.emoji = EMOJI.FINGER
        elif self.count < 5:
            self.emoji = EMOJI.TWO_FINGERS
        elif self.count < 10:
            self.emoji = EMOJI.HAND
        else:
            self.emoji = EMOJI.BOTH_HANDS

    def set_emoji_from_random_out(self):
        self.emoji = EMOJI.FINGER_DOWN


class Pineapple(object):

    open_pineapples = {}

    @classmethod
    def open(cls, chat_id, action, owner):
        logger.info("Pineapple action: %s" % action)
        cls.open_pineapples[chat_id] = Pineapple(action, owner)

    @classmethod
    def close(cls, chat_id):
        del cls.open_pineapples[chat_id]

    @classmethod
    def get(cls, chat_id):
        return cls.open_pineapples[chat_id]

    @classmethod
    def is_open(cls, chat_id):
        return chat_id in cls.open_pineapples.keys()

    def __init__(self, action, owner):
        self.action = action
        self.owner = owner
        self.fingers = {}

    def is_fingers_empty(self):
        return len(self.fingers.keys()) == 0

    def finger_exists(self, user_name):
        return user_name in self.fingers.keys()

    def finger_in(self, user_name):
        logger.info("Finger in from %s" % user_name)
        if self.finger_exists(user_name):
            self.fingers[user_name].increment()
        else:
            self.fingers[user_name] = Finger()

    def finger_out(self, user_name):
        logger.info("Finger out from %s" % user_name)
        if not self.finger_exists(user_name):
            self.fingers[user_name] = Finger()
        self.fingers[user_name].set_out()

    # Messages
    def get_message(self):
        return MESSAGE.NEW_PINEAPPLE.format(self.action)

    def get_close_message(self):
        if self.is_fingers_empty():
            return MESSAGE.NO_ONE
        else:
            return self.get_full_fingers_list_message(closed_hand=True)

    def get_full_fingers_list_message(self, closed_hand=False):
        message = MESSAGE.WHO_WANTS.format(self.action) + '\n'
        if closed_hand:
            message += EMOJI.CLOSED_HAND
        else:
            message += EMOJI.HAND
        message += ' <b>' + self.owner + '</b>\n'
        message += self.get_fingers_in_list_message() + '\n'

        fingers_out = self.get_fingers_out_list_message()
        if fingers_out is not "":
            message += MESSAGE.WHO_DOESNT_WANT.format(self.action) + '\n'
            message += fingers_out
        return message

    def get_short_fingers_list_message(self):
        message = EMOJI.HAND + ' <b>' + self.owner + '</b>\n'
        message += self.get_fingers_in_list_message()
        message += '\n' + self.get_fingers_out_list_message()
        return message

    def get_fingers_in_list_message(self):
        message = ''
        for user_name, finger in self.fingers.items():
            if finger.is_in:
                message += finger.emoji + ' ' + user_name + '\n'
        return message

    def get_fingers_out_list_message(self):
        message = ''
        for user_name, finger in self.fingers.items():
            if not finger.is_in:
                message += finger.emoji + ' ' + user_name + '\n'
        return message
