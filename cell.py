#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QRect, Qt
from math import fabs
from PyQt5.QtGui import QBrush, QColor
from constants import *
from copy import copy


class Cell():
    def __init__(self, x, y, checker, checker_color, cell_color,
                 field_dimension, cell_length, is_king=False, is_chosen=False):
        self.x = x
        self.y = y
        self.checker = checker
        self.checker_color = checker_color
        self.position = False
        self.cell_color = cell_color
        self.positions = []
        self.field_dimension = field_dimension
        self.cell_length = cell_length
        self.is_walking = False
        self.is_king = is_king
        self.is_chosen = is_chosen
        self.rect = QRect(self.x * cell_length, self.y * cell_length, cell_length, cell_length)

    def __str__(self):
        return 'class CELL: ({}, {})'.format(self.x, self.y)

    def is_in_borders(self, x, y):
        return 0 <= x <= self.field_dimension - 1 and 0 <= y <= self.field_dimension - 1

    def find_longest_cut(self, previous_cell, game_field, result_positions, current_player, start_checker):
        positions = self.find_positions_after_cut(previous_cell, game_field, current_player,
                                                  is_king=start_checker.is_king)
        if positions == []:
            if len(start_checker.positions) > 0:
                if len(result_positions) > len(start_checker.positions[0]):
                    start_checker.positions = []
                    start_checker.positions.append(copy(result_positions))
                elif len(result_positions) == len(start_checker.positions[0]):
                    start_checker.positions.append(copy(result_positions))
            else:
                start_checker.positions.append(copy(result_positions))
        else:
            for cell in positions:
                result_positions.append(cell)
                cell.find_longest_cut(self, game_field, result_positions, current_player, start_checker)
                result_positions.remove(cell)

    def find_positions_after_cut(self, previous_cell, game_field, current_player, is_king=False):
        positions = []
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        if previous_cell is not None:
            excess_x = ((previous_cell.y - self.y) // fabs(previous_cell.y - self.y))
            excess_y = ((previous_cell.x - self.x) // fabs(previous_cell.x - self.x))
            directions.remove((excess_x, excess_y))
        if self.checker and self.is_king or is_king:
            for direction in directions:
                checked_x = self.y
                checked_y = self.x
                while True:
                    checked_x += direction[0]
                    checked_y += direction[1]
                    if not self.is_in_borders(checked_x, checked_y) or checked_x + direction[0] < 0 or \
                            checked_x + direction[0] > self.field_dimension - 1 or \
                            checked_y + direction[1] < 0 or checked_y + direction[1] > self.field_dimension - 1:
                        break
                    if game_field.field[checked_x][checked_y].checker:
                        checked_cell = game_field.field[checked_x][checked_y]
                        if checked_cell.checker_color != current_player.color:
                            if not game_field.field[checked_x + direction[0]][checked_y + direction[1]].checker:
                                position_x = checked_x + direction[0]
                                position_y = checked_y + direction[1]
                                while self.is_in_borders(position_x, position_y) and not game_field.field[position_x][
                                    position_y].checker:
                                    positions.append(game_field.field[position_x][position_y])
                                    position_x += direction[0]
                                    position_y += direction[1]
                        break
        else:
            for direction in directions:
                neighboring_x = (self.y + direction[0])
                neighboring_y = (self.x + direction[1])
                new_location_x = neighboring_x + direction[0]
                new_location_y = neighboring_y + direction[1]
                if neighboring_x < 0 or neighboring_x > self.field_dimension - 1 or neighboring_y < 0 or \
                        neighboring_y > self.field_dimension - 1 or new_location_x < 0 or \
                        new_location_x > self.field_dimension - 1 or new_location_y < 0 or new_location_y > self.field_dimension - 1:
                    continue
                enemy_cell = game_field.field[neighboring_x][neighboring_y]
                next_cell = game_field.field[new_location_x][new_location_y]
                if enemy_cell.checker and not next_cell.checker and enemy_cell.checker_color != current_player.color:
                    positions.append(next_cell)
        return positions

    def is_step_possible(self, empty_cell, current_player, game_field):
        if self.checker and self.is_king and not empty_cell.checker:
            if fabs(self.x - empty_cell.x) == fabs(self.y - empty_cell.y):
                enemy_cells = self.get_enemies(empty_cell, game_field)
                return len(enemy_cells) == 0
        else:
            k = DIRECTION_COEFFICIENTS[current_player.color.getRgb()]
            return fabs(self.x - empty_cell.x) == 1 and \
                   self.y - empty_cell.y == k and \
                   empty_cell.cell_color == CELL_BLACK_COLOR and not empty_cell.checker

    def get_enemies(self, empty_cell, game_field):
        start_x = self.y
        last_x = empty_cell.y
        start_y = self.x
        last_y = empty_cell.x
        enemy_cells = []
        if start_x > last_x and start_y > last_y:
            dx = dy = -1
        elif start_x > last_x and start_y < last_y:
            dx = -1
            dy = 1
        elif start_x < last_x and start_y > last_y:
            dx = 1
            dy = -1
        else:
            dx = dy = 1
        while start_x != last_x:
            start_x += dx
            start_y += dy
            if game_field.field[start_x][start_y].checker:
                if game_field.field[start_x][start_y].checker_color != self.checker_color:
                    enemy_cells.append(game_field.field[start_x][start_y])
                else:
                    enemy_cells.append('Not None')
        return enemy_cells

    def find_positions_after_step(self, current_player, game_field):
        positions = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if self.checker and self.is_king:
            for direction in directions:
                position_x = self.y + direction[0]
                position_y = self.x + direction[1]
                while self.is_in_borders(position_x, position_y) and not game_field.field[position_x][
                    position_y].checker:
                    positions.append(game_field.field[position_x][position_y])
                    position_x += direction[0]
                    position_y += direction[1]
        else:
            for direction in directions:
                dir_x, dir_y = direction[0], direction[1]
                if self.y + dir_x < 0 or self.y + dir_x > self.field_dimension - 1 or \
                        self.x + dir_y < 0 or self.x + dir_y > self.field_dimension - 1:
                    continue
                if self.is_step_possible(game_field.field[self.y + dir_x][self.x + dir_y], current_player, game_field):
                    positions.append(game_field.field[self.y + dir_x][self.x + dir_y])
        return positions

    def make_step(self, empty_cell, current_player, game):
        self.is_walking = False
        current_player.remove_checker(self)
        empty_cell.checker_color, self.checker_color = self.checker_color, empty_cell.checker_color
        empty_cell.checker, self.checker = self.checker, empty_cell.checker
        empty_cell.is_king, self.is_king = self.is_king, empty_cell.is_king
        empty_cell.positions, self.positions = self.positions, empty_cell.positions
        empty_cell.positions.remove(empty_cell)
        game.walking_checkers.remove(self)
        game.walking_checkers.append(empty_cell)
        current_player.add_checker(empty_cell)

    def is_correct_cut(self, empty_cell, game_field):
        if self.checker and self.is_king and not empty_cell.checker:
            if fabs(self.x - empty_cell.x) == fabs(self.y - empty_cell.y):
                enemy_cells = self.get_enemies(empty_cell, game_field)
                return len(enemy_cells) == 1 and type(enemy_cells[0]) is Cell

        x = (self.y + empty_cell.y) // 2
        y = (self.x + empty_cell.x) // 2
        return fabs(self.x - empty_cell.x) == fabs(self.y - empty_cell.y) == 2 and \
               not empty_cell.checker and game_field.field[x][y].checker and \
               game_field.field[x][y].checker_color != self.checker_color

    def cut(self, empty_cell, enemy_cells, game):
        x = None
        y = None
        if self.checker and self.is_king:
            if enemy_cells[0] is not None:
                x = enemy_cells[0].y
                y = enemy_cells[0].x
        else:
            x = (self.y + empty_cell.y) // 2
            y = (self.x + empty_cell.x) // 2
        if not (x is None and y is None):
            game.players[game.current_player].remove_checker(game.game_field.field[x][y])
            game.game_field.field[x][y].checker = False
            game.game_field.field[x][y].is_king = False
            game.game_field.field[x][y].checker_color = None
            game.game_field.field[game.chosen_x][game.chosen_y].is_chosen = False
            game.chosen_x, game.chosen_y = empty_cell.y, empty_cell.x
            game.game_field.field[game.chosen_x][game.chosen_y].is_chosen = True
            self.make_step(empty_cell, game.current_player, game)
        game.check_is_someone_winner()

    def check_is_king(self, game_field, is_cut_now):
        if (self.y, self.x) in game_field.king_checkers[self.checker_color.getRgb()] and not is_cut_now and \
                game_field.field[self.y][self.x].checker:
            game_field.field[self.y][self.x].is_king = True

    def draw_cell(self, qPainter):
        qPainter.setBrush(self.cell_color)
        qPainter.drawRect(self.rect)
        if self.checker:
            qPainter.setBrush(self.checker_color)
            qPainter.drawEllipse(self.x * self.cell_length, self.y * self.cell_length, self.cell_length,
                                 self.cell_length)

        if self.is_king:
            qPainter.setBrush(KING_COLOR)
            qPainter.drawEllipse(self.x * self.cell_length + self.cell_length // 4,
                                 self.y * self.cell_length + self.cell_length // 4,
                                 self.cell_length - self.cell_length // 2,
                                 self.cell_length - self.cell_length // 2)
        if self.is_walking:
            brush = QBrush(CHOSE_COLOR)
            brush.setStyle(Qt.DiagCrossPattern)
            qPainter.setBrush(brush)
            qPainter.drawRect(self.rect)

        if self.position:
            brush = QBrush(QColor(255, 255, 0))
            brush.setStyle(Qt.DiagCrossPattern)
            qPainter.setBrush(brush)
            qPainter.drawRect(self.rect)

        if self.is_chosen:
            brush = QBrush(FRAME_COLOR)
            brush.setStyle(Qt.DiagCrossPattern)
            qPainter.setBrush(brush)
            qPainter.drawRect(self.rect)
