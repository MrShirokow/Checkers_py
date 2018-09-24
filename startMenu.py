#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from os import path
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QLabel, QLineEdit, QApplication, QMainWindow, QPushButton, QMessageBox, qApp, QComboBox
from board import Board
from constants import CHECKER_WHITE_COLOR, CHECKER_BLACK_COLOR, SCRIPT_DIR


class StartMenu(QMainWindow):
    """
    Класс стартового окна меню.
    """

    def __init__(self):
        super(StartMenu, self).__init__()
        self.game_mode = None
        self.field_dimension = None
        self.really_player_color = None
        self.initUI()

    def initUI(self):
        dimension_label = QLabel('Выберите \nразмерность: ', self)
        dimension_label.adjustSize()
        dimension_label.move(30, 20)
        self.dimension_box = QComboBox(self)
        self.dimension_box.move(30, 55)
        dimensions = [str(x) for x in range(6, 51) if x % 2 == 0]
        self.dimension_box.addItems(dimensions)
        self.dimension_box.activated[str].connect(self.set_dimension)
        game_mode_label = QLabel('Выберите игровой мод: ', self)
        game_mode_label.adjustSize()
        game_mode_label.move(320, 30)
        self.game_mode_box = QComboBox(self)
        self.game_mode_box.addItem('PvP')
        self.game_mode_box.addItem('PvE')
        self.game_mode_box.move(320, 55)
        self.game_mode_box.activated[str].connect(self.set_game_mode)
        game_mode_label = QLabel('Выберите цвет игрока: ', self)
        game_mode_label.adjustSize()
        game_mode_label.move(150, 30)
        self.start_player_color_box = QComboBox(self)
        self.start_player_color_box.addItem('White')
        self.start_player_color_box.addItem('Black')
        self.start_player_color_box.move(170, 55)
        self.start_player_color_box.activated[str].connect(self.set_start_player_color)
        start_btn = QPushButton("Начать игру", self)
        start_btn.clicked.connect(self.start_game)
        start_btn.move(100, 120)
        load_game_btn = QPushButton('Загрузить игру', self)
        load_game_btn.clicked.connect(self.load_game)
        load_game_btn.move(200, 120)
        exit_btn = QPushButton('Выход', self)
        exit_btn.clicked.connect(qApp.quit)
        exit_btn.move(300, 120)
        help_button = QPushButton('Help', self)
        help_button.clicked.connect(self.show_help)
        help_button.move(200, 150)
        self.setGeometry(300, 300, 500, 200)
        resources = path.join(SCRIPT_DIR, 'resources')
        self.setWindowIcon(QIcon(path.join(resources, 'checker.png')))
        self.setWindowTitle('Start menu')
        self.setFixedSize(self.size())

    def show_help(self):
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle('Help')
        help_path = path.join(SCRIPT_DIR, 'resources', 'help.jpg')
        self.msgBox.setWindowIcon(QIcon(help_path))
        self.msgBox.setText("Игра 100-клеточный шашки (международные)\n\n"
                            "В открывшемся окне нужно выбрать размерность поля, игровой мод и цвет игрока "
                            "(нужно в случае, когда один из игроков - искусственный интеллект)\n\n"
                            "Управление осуществляется мышью, выбирая шашку, затем кликая на клетку, "
                            "на которую хотите сделать ход.\n"
                            "Успехов!")
        self.msgBox.exec()

    def set_start_player_color(self, color_text):
        """
        Метод устанавливает стартовый цвет игрока.
        Параметр - цвет в формате строки.
        """
        colors = {'White': CHECKER_WHITE_COLOR, 'Black': CHECKER_BLACK_COLOR}
        try:
            self.really_player_color = colors[color_text]
        except KeyError:
            raise KeyError("Error color!")

    def set_game_mode(self, game_mode):
        """
        Метод устанавливает игровой мод (PvP/PvE).
        Параметр - игровой мод.
        """
        self.game_mode = game_mode

    def set_dimension(self, dimension):
        """
        Метод устанавливает размерность поля.
        Параметр - размерность поля.
        """
        try:
            self.field_dimension = int(dimension)
        except TypeError:
            raise TypeError('This is error type!')
        except ValueError:
            raise ValueError("This is error value!")

    def start_game(self, run_in_test=False):
        """
        Метод, на который опирается кнопка начала игры. После нажатия запускается партия.
        Параметр - флаг, который по умолчанию false, за исключением случаев тестирования.
        (Сделано, чтобы при тестировании не открывались всплывающие окна).
        """
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle('Attention!')
        attention_path = path.join(SCRIPT_DIR, 'resources', 'attention.png')
        self.msgBox.setWindowIcon(QIcon(attention_path))
        self.msgBox.setIcon(QMessageBox.Information)
        if self.game_mode is None:
            self.msgBox.setText('Choose game mode!')
            if not run_in_test:
                self.msgBox.exec()
        elif self.really_player_color is None:
            self.msgBox.setText('Choose start player color!')
            if not run_in_test:
                self.msgBox.exec()
        elif self.field_dimension is None:
            self.msgBox.setText("Choose field dimension!")
            if not run_in_test:
                self.msgBox.exec()
        else:
            self.close()
            self.main_window = Board(self.field_dimension, white_set=set(), black_set=set(),
                                     game_mode=self.game_mode, really_player_color=self.really_player_color)
            self.main_window.show()

    def load_game(self, run_in_test=False):
        """
        Метод загрузки игры.
        Параметр - флаг, который по умолчанию false, за исключением случаев тестирования.
        (Сделано, чтобы при тестировании не открывались всплывающие окна).
        """
        with open('load_game.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        if text == '':
            self.mesBox = QMessageBox()
            self.mesBox.setWindowTitle('Attention!')
            attention_path = path.join(SCRIPT_DIR, 'resources', 'attention.png')
            self.mesBox.setWindowIcon(QIcon(attention_path))
            self.mesBox.setIcon(QMessageBox.Information)
            self.mesBox.setText("No saved game.")
            self.mesBox.exec()
        else:
            white_set = set()
            black_set = set()
            dict = {'True': True,
                    'False': False,
                    'None': None}
            parts = text.split('@')
            field_dimension = int(parts[0])
            parts[1] = parts[1].replace('(', '').replace(')', '').split(',')
            current_player_color = QColor(int(parts[1][0]), int(parts[1][1]), int(parts[1][2]))
            is_cut_now = dict[parts[2].replace('\n', '')]
            chosen_x = self.get_value(parts[3].replace('\n', ''), dict)
            chosen_y = self.get_value(parts[4].replace('\n', ''), dict)
            mouse_x = self.get_value(parts[5].replace('\n', ''), dict)
            mouse_y = self.get_value(parts[6].replace('\n', ''), dict)
            game_mode = parts[7].replace('\n', '')
            parts[8] = parts[8].replace('(', '').replace(')', '').split(',')
            really_player_color = QColor(int(parts[8][0]), int(parts[8][1]), int(parts[8][2]))
            from cell import Cell
            parts[9] = list(filter(None, parts[9].split('\n')))
            cells_for_load = [["0"] * field_dimension for _ in range(field_dimension)]
            x = y = 0
            for options in parts[9]:
                options = options.split('#')
                if options[3] == 'None':
                    color = dict[options[3]]
                else:
                    options[3] = options[3].replace('(', '').replace(')', '').split(',')
                    color = QColor(int(options[3][0]), int(options[3][1]), int(options[3][2]))
                options[4] = options[4].replace('(', '').replace(')', '').split(',')
                cells_for_load[x][y] = Cell(int(options[0]),
                                            int(options[1]),
                                            dict[options[2]],
                                            color,
                                            QColor(int(options[4][0]),
                                                   int(options[4][1]),
                                                   int(options[4][2])),
                                            int(options[5]),
                                            int(options[6]),
                                            dict[options[7]],
                                            dict[options[8]])

                if cells_for_load[x][y].checker and CHECKER_WHITE_COLOR == color:
                    white_set.add(cells_for_load[x][y])
                if cells_for_load[x][y].checker and CHECKER_BLACK_COLOR == color:
                    black_set.add(cells_for_load[x][y])

                y += 1
                if y == field_dimension:
                    y = 0
                    x += 1

            self.close()
            self.board = Board(field_dimension, current_player_color, is_cut_now,
                               cells_for_load, white_set, black_set,
                               chosen_x, chosen_y, mouse_x, mouse_y, game_mode, really_player_color)
            if not run_in_test:
                self.board.show()

    def get_value(self, string_value, dict):
        """
        Метод возвращает значение по его строковому представлению. Сделано для загрузки игры.
        Параметры: строковое значение и словарь, в котором по строке можно получить значение, если ключ валидный.
        """
        try:
            if string_value in dict.keys():
                return dict[string_value]
            value = int(string_value)
            return value
        except ValueError:
            raise ValueError('This is error value!')
        except TypeError:
            raise TypeError('This is error type!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = StartMenu()
    start_window.show()
    sys.exit(app.exec_())
