#!/usr/bin/env python
# -*- coding: utf-8 -*-


from constants import *


class Player:
    """
    Класс игрока.
    """

    def __init__(self, color, is_really_player, checkers_set):
        self.is_really_player = is_really_player
        self.checkers_count = len(checkers_set)
        self.color = color
        self.checkers = checkers_set
        self.is_complete = False

    def add_checker(self, checker):
        """
        Метод добавляет шашку в список шашек игрока.
        Параметры: шашка для добавления.
        """
        self.checkers.add(checker)
        self.checkers_count = len(self.checkers)

    def remove_checker(self, checker):
        """
        Метод удаляет шашку из списка шашек игрока.
        Параметры: шашка для удаления.
        """
        self.checkers.remove(checker)
        self.checkers_count = len(self.checkers)
