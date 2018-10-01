#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cell import *
from constants import *


class Field:
    """
    Класс игрового поля.
    """

    def __init__(self, white_player, black_player, field_dimension, cell_length, cells_for_load=None):
        self.white_player = white_player
        self.black_player = black_player
        self.field_dimension = field_dimension
        self.cell_length = cell_length
        if cells_for_load is None:
            self.field = self.create_start_field()
        else:
            self.field = cells_for_load
        self.king_checkers = self.create_king_cells()

    def get_player_by_color(self, color):
        """
        Метод возвращает игрока по цвету.
        """
        if self.white_player.color == color:
            return self.white_player
        return self.black_player

    def create_start_field(self):
        """
        Метод создаёт стартовое поле.
        """
        game_field = [["0"] * self.field_dimension for _ in range(self.field_dimension)]
        x = y = 0
        for field_x in range(self.field_dimension):
            for field_y in range(self.field_dimension):
                if 0 <= field_x < self.field_dimension // 2 - 1:
                    checker = False
                    cell_color = CELL_WHITE_COLOR
                    cell = Cell(x, y, checker, None, cell_color, self.field_dimension, self.cell_length)

                    if (field_x + field_y) % 2 == 1:
                        checker = True
                        cell_color = CELL_BLACK_COLOR
                        cell = Cell(x, y, checker, CHECKER_BLACK_COLOR, cell_color, self.field_dimension,
                                    self.cell_length)
                        self.black_player.add_checker(cell)
                    game_field[field_x][field_y] = cell

                elif self.field_dimension // 2 - 1 <= field_x <= self.field_dimension // 2:
                    cell_color = CELL_WHITE_COLOR
                    if (field_x + field_y) % 2 == 1:
                        cell_color = CELL_BLACK_COLOR
                    game_field[field_x][field_y] = Cell(x, y, False, None, cell_color, self.field_dimension,
                                                        self.cell_length)

                else:
                    checker = False
                    cell_color = CELL_WHITE_COLOR
                    cell = Cell(x, y, checker, None, cell_color, self.field_dimension, self.cell_length)

                    if (field_x + field_y) % 2 == 1:
                        checker = True
                        cell_color = CELL_BLACK_COLOR
                        cell = Cell(x, y, checker, CHECKER_WHITE_COLOR, cell_color, self.field_dimension,
                                    self.cell_length)
                        self.white_player.add_checker(cell)
                    game_field[field_x][field_y] = cell

                x += 1
            y += 1
            x = 0

        return game_field

    def draw_field(self, qpainter):
        """
        Метод отрисовки.
        """
        for field_x in range(self.field_dimension):
            for field_y in range(self.field_dimension):
                self.field[field_x][field_y].draw_cell(qpainter)

    def create_king_cells(self):
        """
        Метод генерирует клетки, при заходе на которые шашка становится дамкой.
        """
        kings_black_checkers = []
        kings_white_checkers = []
        field_x = 0
        for field_y in range(self.field_dimension):
            kings_white_checkers.append((field_x, field_y))
        field_x = self.field_dimension - 1
        for field_y in range(self.field_dimension):
            kings_black_checkers.append((field_x, field_y))

        return {CHECKER_BLACK_COLOR.getRgb(): kings_black_checkers,
                CHECKER_WHITE_COLOR.getRgb(): kings_white_checkers}
