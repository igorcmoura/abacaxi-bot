#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from diskcache import Cache

from .constants import EMOJI, MESSAGE
from .logger import logger


def to_bold(text):
    multiplication_sign = "\u02df"
    clean_text = text.replace("*", multiplication_sign)
    return "*" + clean_text + "*"


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

    def set_middle_finger(self):
        self.is_in = True
        self.count = 0
        self.update_emoji()

    def update_emoji(self):
        if self.is_in:
            self.set_emoji_from_finger_count()
        else:
            self.set_emoji_from_random_out()

    def set_emoji_from_finger_count(self):
        if self.count == 0:
            self.emoji = EMOJI.MIDDLE_FINGER
        elif self.count < 2:
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

    open_pineapples = Cache('open_pineapples')

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
    def update(cls, chat_id, pineapple):
        cls.open_pineapples[chat_id] = pineapple

    @classmethod
    def is_open(cls, chat_id):
        return chat_id in cls.open_pineapples

    def __init__(self, action, owner):
        self.action = action
        self.owner = owner
        self.fingers = {}

    def is_fingers_empty(self):
        return len(self.fingers) == 0

    def finger_exists(self, user_name):
        return user_name in self.fingers.keys()

    def finger_in(self, user_name):
        logger.info("Finger in from %s" % user_name)
        if user_name == self.owner:
            return
        if self.finger_exists(user_name):
            self.fingers[user_name].increment()
        else:
            self.fingers[user_name] = Finger()

    def finger_out(self, user_name):
        logger.info("Finger out from %s" % user_name)
        if user_name == self.owner:
            return
        if not self.finger_exists(user_name):
            self.fingers[user_name] = Finger()
        self.fingers[user_name].set_out()

    def middle_finger(self, user_name):
        logger.info("Finger middle finger from %s" % user_name)
        if user_name == self.owner:
            return
        if not self.finger_exists(user_name):
            self.fingers[user_name] = Finger()
        self.fingers[user_name].set_middle_finger()

    # Messages
    def get_open_message(self):
        return MESSAGE.NEW_PINEAPPLE.format(to_bold(self.action))

    def get_close_message(self):
        if self.is_fingers_empty():
            return MESSAGE.NO_ONE
        else:
            return self.get_fingers_list_message(closed=True)

    def get_fingers_list_message(self, closed=False):

        if closed:
            message = MESSAGE.WHO_WANTS_CLOSED + '\n'
            message += EMOJI.CLOSED_HAND
        else:
            message = MESSAGE.WHO_WANTS_OPEN + '\n'
            message += EMOJI.HAND
        message += ' ' + to_bold(self.owner) + '\n'
        message += self.get_fingers_in_list_message() + '\n'

        fingers_out = self.get_fingers_out_list_message()
        if fingers_out is not "":
            if closed:
                message += MESSAGE.WHO_DOESNT_WANT_CLOSED + '\n'
            else:
                message += MESSAGE.WHO_DOESNT_WANT_OPEN + '\n'
            message += fingers_out
        return message

    def get_short_fingers_list_message(self):
        message = EMOJI.HAND + " " + to_bold(self.owner) + "\n"
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
