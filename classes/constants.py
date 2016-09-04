#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class EMOJI:
    FINGER = "\u261d\ufe0f"
    TWO_FINGERS = "\u270c"
    MIDDLE_FINGER = "\ud83d\udd95"
    HAND = "\ud83d\udd90"
    BOTH_HANDS = "\ud83d\ude4c"
    CLOSED_HAND = "\ud83d\udc4a"
    PINEAPPLE = "\ud83c\udf4d"
    SADFACE = "\ud83d\ude22"

    FINGER_DOWN = "\ud83d\udc4e"


class MESSAGE:
    ALREADY_OPEN = "Já tem um abacaxi aberto:\n{0}"
    NOT_YET_OPEN = "Nenhum abacaxi aberto."

    WHO_WANTS_OPEN = "O abacaxi vai fechar:"
    WHO_DOESNT_WANT_OPEN = "E quem vai sobrar:"
    WHO_WANTS_CLOSED = "O abacaxi se fechou:"
    WHO_DOESNT_WANT_CLOSED = "E quem não entrou:"

    FINGER = EMOJI.FINGER

    NO_MORE_FINGERS_IN_HAND = "Você não tem mais dedos em suas mãos."
    NO_ONE = "Todos ignoraram o abacaxi. " + EMOJI.SADFACE
    NEW_PINEAPPLE = "Quem quer {0}\npõe o dedo aqui,\nque já vai fechar\no abacaxi. " + EMOJI.PINEAPPLE
    USAGE_OPEN = "Uso:\n/abacaxi <ação>"

    HELP = "O Abacaxi Bot irá te ajudar a fazer uma votação usando a brincadeira do abacaxi. "
    HELP += "Para isso, use os seguintes comandos:\n"
    HELP += "/abacaxi <ação> - para abrir um novo abacaxi\n"
    HELP += "/dedo - para colocar o dedo no abacaxi\n"
    HELP += "/dedofora - para mostrar que você não quer entrar\n"
    HELP += "/quem - para ver quem está no abacaxi\n"
    HELP += "/fechar - para fechar o abacaxi\n"
