#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QTimer
from cell import *
from endGameWindow import EndGameWindow
from field import Field
from player import Player
from math import fabs
from constants import *
from random import choice
from copy import deepcopy


class BoardWidget(QFrame):
    """
    Основной класс игры.
    """

    def __init__(self, board, field_dimension, cell_length, win_width,
                 current_player_color=None, is_cut_now=False,
                 cells_for_load=None, white_set=set(), black_set=set(),
                 chosen_x=None, chosen_y=None,
                 mouse_x=None, mouse_y=None,
                 game_mode=None, really_player_color=None):
        super(BoardWidget, self).__init__()
        self.walking_checkers = []
        self.field_dimension = field_dimension
        self.cell_length = cell_length
        self.really_player_color = really_player_color
        self.game_mode = game_mode
        self.cells_for_load = cells_for_load
        self.white_set = white_set
        self.black_set = black_set
        self.board = board
        self.timer = QTimer()
        white_player = Player(CHECKER_WHITE_COLOR, True, self.white_set)
        black_player = Player(CHECKER_BLACK_COLOR, True, self.black_set)
        self.game_field = Field(white_player, black_player, field_dimension, self.cell_length, cells_for_load)
        if current_player_color is None:
            self.current_player = self.game_field.white_player
        else:
            self.current_player = self.game_field.get_player_by_color(current_player_color)
        if self.really_player_color == CHECKER_BLACK_COLOR:
            if self.game_mode == 'PvE':
                white_player.is_really_player = False
        else:
            if self.game_mode == 'PvE':
                black_player.is_really_player = False
        self.chosen_x = chosen_x
        self.chosen_y = chosen_y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.is_white_winner = False
        self.is_black_winner = False
        self.is_cut_now = is_cut_now
        self.win_width = self.win_height = win_width
        self.setGeometry(300, 100, self.win_width, self.win_height)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        game_field = self.game_field
        game_field.draw_field(qp)
        self.players = {game_field.white_player: game_field.black_player,
                        game_field.black_player: game_field.white_player}

        # Ищем шашки, которыми можем рубить или просто ходить
        if not self.timer.isActive():
            if not self.is_cut_now and len(self.walking_checkers) == 0:
                result_positions = []
                for checker in self.current_player.checkers:
                    # checker.positions = checker.find_positions_after_cut(None, game_field, self.current_player)
                    checker.find_longest_cut(None, game_field, result_positions, self.current_player, checker)
                    way = []
                    for list in checker.positions:
                        for c in list:
                            c.position = True
                            way.append(c)
                    checker.positions = way
                    if len(checker.positions) > 0:
                        checker.is_walking = True
                        self.walking_checkers.append(checker)
                if len(self.walking_checkers) == 0:
                    for checker in self.current_player.checkers:
                        checker.positions = checker.find_positions_after_step(self.current_player, self.game_field)
                        if len(checker.positions) > 0:
                            checker.is_walking = True
                            self.walking_checkers.append(checker)

            # Проверка на партию в ничью
            if len(self.walking_checkers) == 0 and len(self.current_player.checkers) != 0:
                self.board.close()
                self.end_window = EndGameWindow('Nobody is winner...')
                self.end_window.show()

            # Логика игры
            if self.mouse_x is not None or not self.current_player.is_really_player:
                column, row = self.mouse_x, self.mouse_y
                if not self.current_player.is_really_player:
                    # Заходим, если игрок - ПК
                    chosen_cell = choice(self.walking_checkers)
                    chosen_cell.is_chosen = True
                    self.chosen_x, self.chosen_y = chosen_cell.y, chosen_cell.x
                    # empty_cell = choice(chosen_cell.positions)
                    empty_cell = chosen_cell.positions[0]
                    row, column = empty_cell.y, empty_cell.x
                    self.current_player.is_complete = False

                if self.chosen_x is None:
                    # Первичный заход, выбор шашки
                    self.current_player.is_complete = False
                    if not game_field.field[row][column].checker:
                        pass
                    else:
                        chosen_cell = game_field.field[row][column]
                        if chosen_cell in self.current_player.checkers and chosen_cell.is_walking:
                            self.chosen_x, self.chosen_y = row, column
                            chosen_cell.is_chosen = True
                else:
                    # Проверяем на сруб
                    if game_field.field[self.chosen_x][self.chosen_y].is_correct_cut(game_field.field[row][column],
                                                                                     game_field) and \
                            game_field.field[row][column] in game_field.field[self.chosen_x][self.chosen_y].positions:
                        self.is_cut_now = True
                        enemy_cells = game_field.field[self.chosen_x][self.chosen_y].get_enemies(
                            game_field.field[row][column], game_field)
                        previous_cell = game_field.field[self.chosen_x][self.chosen_y]
                        game_field.field[self.chosen_x][self.chosen_y].cut(game_field.field[row][column],
                                                                           enemy_cells, self)
                        positions = game_field.field[row][column].find_positions_after_cut(previous_cell, game_field,
                                                                                           self.current_player)
                        if len(positions) == 0:
                            self.current_player.is_complete = True
                            game_field.field[self.chosen_x][self.chosen_y].is_chosen = False
                            self.chosen_x, self.chosen_y = None, None
                            self.is_cut_now = False
                        game_field.field[row][column].check_is_king(game_field, self.is_cut_now)
                    elif not self.is_cut_now:
                        # Проверяем на холостой ход
                        if game_field.field[self.chosen_x][self.chosen_y].is_step_possible(
                                game_field.field[row][column], self.current_player, game_field) and \
                                game_field.field[row][column] in game_field.field[self.chosen_x][
                            self.chosen_y].positions:
                            game_field.field[self.chosen_x][self.chosen_y].make_step(game_field.field[row][column],
                                                                                     self.current_player, self)
                            self.current_player.is_complete = True
                            game_field.field[row][column].check_is_king(game_field, self.is_cut_now)
                        game_field.field[self.chosen_x][self.chosen_y].is_chosen = False
                        self.chosen_x, self.chosen_y = None, None

                    if self.current_player.is_complete:
                        # ----------------------------------------------------------------------
                        self.walking_checkers = []
                        if not self.is_cut_now:
                            for i in range(self.field_dimension):
                                for j in range(self.field_dimension):
                                    self.game_field.field[i][j].position = False
                                    self.game_field.field[i][j].is_walking = False
                                    self.game_field.field[i][j].positions = []
                                    self.game_field.field[i][j].is_chosen = False
                        # Проверка завершения хода игрока
                        other_player = self.players[self.current_player]
                        if self.current_player.is_really_player:
                            self.timer.setSingleShot(True)
                            self.timer.start(600)
                        self.current_player = other_player
                self.mouse_x = None
                self.mouse_y = None

        self.update()
        qp.end()

        if self.is_black_winner or self.is_white_winner:
            self.show_result_window()

    def is_in_positions(self, checker, positions):
        for list in positions:
            if checker in list:
                return True
        return False

    def show_result_window(self):
        text = 'White player is winner!'
        if self.is_black_winner:
            text = 'Black player is winner!'
        self.board.close()
        self.end_window = EndGameWindow(text)
        self.end_window.show()

    def mousePressEvent(self, QMouseEvent):
        self.mouse_x = QMouseEvent.pos().x() // self.cell_length
        self.mouse_y = QMouseEvent.pos().y() // self.cell_length

    def check_is_someone_winner(self):
        if self.game_field.white_player.checkers_count == 0:
            self.is_black_winner = True
        elif self.game_field.black_player.checkers_count == 0:
            self.is_white_winner = True
