#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class EMOJI:
    FINGER = "\u261d\ufe0f"
    TWO_FINGERS = "\u270c"
    HAND = "\ud83d\udd90"
    BOTH_HANDS = "\ud83d\ude4c"
    CLOSED_HAND = "\ud83d\udc4a"
    PINEAPPLE = "\ud83c\udf4d"
    SADFACE = "\ud83d\ude22"

    FINGER_DOWN = "\ud83d\udc4e"


class MESSAGE:
    ALREADY_OPEN = "Já tem um abacaxi aberto:\n{0}"
    NOT_YET_OPEN = "Nenhum abacaxi aberto."

    WHO_WANTS = "Quem quer <b>{0}</b>:"
    WHO_DOESNT_WANT = "Quem não quer <b>{0}</b>:"

    FINGER = EMOJI.FINGER

    NO_MORE_FINGERS_IN_HAND = "Você não tem mais dedos em suas mãos."
    NO_ONE = "Todos ignoraram o abacaxi. " + EMOJI.SADFACE
    NEW_PINEAPPLE = "Quem quer <b>{0}</b>\npõe o dedo aqui,\nque já vai fechar\no abacaxi. " + EMOJI.PINEAPPLE
    USAGE_OPEN = "Uso:\n/abacaxi <ação>"
