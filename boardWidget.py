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
        white_player = Player(CHECKER_WHITE_COLOR, False, self.white_set)
        black_player = Player(CHECKER_BLACK_COLOR, False, self.black_set)
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
        self.win_width = win_width
        self.setGeometry(300, 100, self.win_width, self.win_width)

    def paintEvent(self, q_paint_event):
        qPainter = QPainter()
        qPainter.begin(self)
        self.main(qPainter)
        self.update()
        qPainter.end()
        if self.is_black_winner or self.is_white_winner:
            self.show_result_window()

    def main(self, qPainter):
        self.game_field.draw_field(qPainter)
        self.players = {self.game_field.white_player: self.game_field.black_player,
                        self.game_field.black_player: self.game_field.white_player}

        if not self.timer.isActive():
            if not self.is_cut_now and len(self.walking_checkers) == 0:
                self.find_walking_checkers()

            if len(self.walking_checkers) == 0 and len(self.current_player.checkers) != 0:
                self.board.close()
                self.end_window = EndGameWindow('Nobody is winner...')
                self.end_window.show()

            if self.mouse_x is not None or not self.current_player.is_really_player:
                column, row = self.mouse_x, self.mouse_y

                if not self.current_player.is_really_player:
                    chosen_cell = choice(self.walking_checkers)
                    chosen_cell.is_chosen = True
                    self.chosen_x, self.chosen_y = chosen_cell.y, chosen_cell.x
                    empty_cell = choice(chosen_cell.positions)
                    row, column = empty_cell.y, empty_cell.x
                    self.current_player.is_complete = False

                if self.chosen_x is None:
                    self.current_player.is_complete = False
                    if not self.game_field.field[row][column].checker:
                        pass
                    else:
                        chosen_cell = self.game_field.field[row][column]
                        if chosen_cell in self.current_player.checkers and chosen_cell.is_walking:
                            self.chosen_x, self.chosen_y = row, column
                            chosen_cell.is_chosen = True
                else:
                    if self.game_field.field[self.chosen_x][self.chosen_y].is_correct_cut(
                            self.game_field.field[row][column],
                            self.game_field):
                        self.cut_move(row, column)
                    elif not self.is_cut_now:
                        self.make_step(row, column)

                    if self.current_player.is_complete:
                        self.change_player()
                self.mouse_x = None
                self.mouse_y = None

    def find_walking_checkers(self):
        result_positions = []
        max_len = 0
        for checker in self.current_player.checkers:
            checker.find_longest_cut(None, self.game_field, result_positions, self.current_player, checker)
            current_len = max(len(list) for list in checker.positions)
            max_len = max(current_len, max_len)
        for checker in self.current_player.checkers:
            way = []
            if max_len != 0:
                for list in checker.positions:
                    if len(list) == max_len:
                        if list[0] not in way:
                            way.append(list[0])
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

    def cut_move(self, checked_x, checked_y):
        if self.game_field.field[checked_x][checked_y] in self.game_field.field[self.chosen_x][self.chosen_y].positions:
            self.is_cut_now = True
            previous_cell = self.game_field.field[self.chosen_x][self.chosen_y]
            enemy_cells = self.game_field.field[self.chosen_x][self.chosen_y].get_enemies(
                self.game_field.field[checked_x][checked_y], self.game_field)
            self.game_field.field[self.chosen_x][self.chosen_y].cut(self.game_field.field[checked_x][checked_y],
                                                                    enemy_cells, self)
            result_positions = []
            self.game_field.field[self.chosen_x][self.chosen_y].positions = []
            self.game_field.field[self.chosen_x][self.chosen_y].find_longest_cut(previous_cell, self.game_field,
                                                                                 result_positions,
                                                                                 self.current_player,
                                                                                 self.game_field.field[
                                                                                     self.chosen_x][self.chosen_y])

            max_len = max(len(list) for list in self.game_field.field[self.chosen_x][self.chosen_y].positions)
            way = []
            if max_len != 0:
                for list in self.game_field.field[self.chosen_x][self.chosen_y].positions:
                    if len(list) == max_len:
                        if list[0] not in way:
                            way.append(list[0])
            self.game_field.field[self.chosen_x][self.chosen_y].positions = way
            if len(self.game_field.field[checked_x][checked_y].positions) == 0:
                self.current_player.is_complete = True
                self.game_field.field[checked_x][checked_y].is_chosen = False
                self.chosen_x, self.chosen_y = None, None
                self.is_cut_now = False
            self.game_field.field[checked_x][checked_y].check_is_king(self.game_field, self.is_cut_now)

    def make_step(self, checked_x, checked_y):
        if self.game_field.field[checked_x][checked_y] in self.game_field.field[self.chosen_x][self.chosen_y].positions:
            if self.game_field.field[self.chosen_x][self.chosen_y].is_step_possible(
                    self.game_field.field[checked_x][checked_y],
                    self.current_player,
                    self.game_field):
                self.game_field.field[self.chosen_x][self.chosen_y].move(self.game_field.field[checked_x][checked_y],
                                                                         self.current_player, self)
                self.current_player.is_complete = True
                self.game_field.field[checked_x][checked_y].check_is_king(self.game_field, self.is_cut_now)
        self.game_field.field[self.chosen_x][self.chosen_y].is_chosen = False
        self.chosen_x, self.chosen_y = None, None

    def change_player(self):
        self.walking_checkers = []
        if not self.is_cut_now:
            for i in range(self.field_dimension):
                for j in range(self.field_dimension):
                    self.game_field.field[i][j].is_walking = False
                    self.game_field.field[i][j].positions = []
                    self.game_field.field[i][j].is_chosen = False

        other_player = self.players[self.current_player]
        if self.current_player.is_really_player:
            self.timer.setSingleShot(True)
            self.timer.start(600)
        self.current_player = other_player

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
