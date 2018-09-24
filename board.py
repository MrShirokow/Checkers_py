#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp
from boardWidget import BoardWidget
from constants import USER32, SCRIPT_DIR
from os import path


class Board(QMainWindow):
    """
    Класс главного окошка, в котором главным виджетом является boardWidget.
    """
    def __init__(self, field_dimension, current_player_color=None,
                 is_cut_now=False, cells_for_load=None,
                 white_set=set(), black_set=set(),
                 chosen_x=None, chosen_y=None,
                 mouse_x=None, mouse_y=None,
                 game_mode=None, really_player_color=None):
        super().__init__()
        self.field_dimension = field_dimension
        self.really_player_color = really_player_color
        self.current_player_color = current_player_color
        self.is_cut_now = is_cut_now
        self.cells_for_load = cells_for_load
        self.white_set = white_set
        self.black_set = black_set
        self.chosen_x = chosen_x
        self.chosen_y = chosen_y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.game_mode = game_mode
        self.cell_length = (USER32.GetSystemMetrics(1) - 150) // field_dimension
        self.win_width = self.win_height = field_dimension * self.cell_length
        self.initUI()

    def initUI(self):
        """
        Инициализация некоторых полей класса.
        """
        resources = path.join(SCRIPT_DIR, 'resources')
        save_game_act = QAction(QIcon(path.join(resources, 'save.png')), 'Save game', self)
        save_game_act.triggered.connect(self.save_game)
        exit_act = QAction(QIcon(path.join(resources, 'exit.png')), 'Exit', self)
        exit_act.triggered.connect(qApp.quit)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(save_game_act)
        fileMenu.addAction(exit_act)

        self.board_widget = BoardWidget(self, self.field_dimension, self.cell_length,
                                        self.win_width, self.current_player_color,
                                        self.is_cut_now, self.cells_for_load,
                                        self.white_set, self.black_set,
                                        self.chosen_x, self.chosen_y,
                                        self.mouse_x, self.mouse_y,
                                        self.game_mode, self.really_player_color)
        self.setGeometry(300, 50, self.win_width, self.win_height + 17 * menuBar.geometry().height() / 20)
        self.setCentralWidget(self.board_widget)
        self.setWindowTitle('Checkers')
        self.setWindowIcon(QIcon(path.join(resources, 'checker.png')))
        self.setFixedSize(self.size())

    def save_game(self):
        """
        Метод сохранения игры.
        """
        with open('load_game.txt', 'w', encoding='utf-8') as f:
            f.truncate()
            f.write(('{}\n' + '@{}\n' * 8).format(self.field_dimension,
                                                  self.board_widget.current_player.color.getRgb(),
                                                  self.board_widget.is_cut_now,
                                                  self.board_widget.chosen_x,
                                                  self.board_widget.chosen_y,
                                                  self.board_widget.mouse_x,
                                                  self.board_widget.mouse_y,
                                                  self.game_mode,
                                                  self.board_widget.really_player_color.getRgb()))
            f.write('@')
            for x in range(self.field_dimension):
                for y in range(self.field_dimension):
                    cell = self.board_widget.game_field.field[x][y]
                    if cell.checker_color is None:
                        checker_color = None
                    else:
                        checker_color = cell.checker_color.getRgb()
                    if cell.cell_color is None:
                        cell_color = None
                    else:
                        cell_color = cell.cell_color.getRgb()

                    f.write(('{}#' * 9).format(cell.x, cell.y, cell.checker, checker_color, cell_color,
                                               cell.field_dimension, cell.cell_length, cell.is_king,
                                               cell.is_chosen) + '\n')
