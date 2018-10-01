import unittest
from player import *
from cell import *
from field import *
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QBrush, QColor
from startMenu import *
from os import path


class StartTests(unittest.TestCase):
    def test_add_and_remove_checker(self):
        player = Player(CHECKER_WHITE_COLOR, set())
        self.assertEqual(0, player.checkers_count)
        checker_1 = Cell(3, 4, True, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 10, 50)
        checker_2 = Cell(7, 1, True, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 10, 50)
        checker_3 = Cell(11, 3, True, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 10, 50)
        player.add_checker(checker_1)
        player.add_checker(checker_2)
        player.add_checker(checker_3)
        self.assertEqual(3, player.checkers_count)
        self.assertEqual(True, checker_1 in player.checkers)
        self.assertEqual(True, checker_2 in player.checkers)
        self.assertEqual(True, checker_3 in player.checkers)
        player.remove_checker(checker_1)
        self.assertEqual(2, player.checkers_count)
        self.assertEqual(False, checker_1 in player.checkers)
        player.remove_checker(checker_3)
        self.assertEqual(False, checker_3 in player.checkers)
        self.assertEqual(1, player.checkers_count)

    def test_get_player_by_color(self):
        field_1 = Field(Player(CHECKER_WHITE_COLOR, set()), Player(CHECKER_BLACK_COLOR, set()), 10, 50)
        player_1 = field_1.get_player_by_color(CHECKER_WHITE_COLOR)
        self.assertEqual(True, player_1 == field_1.white_player)
        player_2 = field_1.get_player_by_color(CHECKER_BLACK_COLOR)
        self.assertEqual(True, player_2 == field_1.black_player)

    def test_is_in_borders(self):
        checker_1 = Cell(3, 4, True, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 10, 50)
        checker_2 = Cell(7, 1, True, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 10, 50)
        checker_3 = Cell(11, 3, True, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 10, 50)
        checker_4 = Cell(50, 1, False, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 50, 50)
        checker_5 = Cell(6, -10, False, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 32, 50)
        checker_6 = Cell(49, 49, False, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 50, 50)
        checker_7 = Cell(0, 0, False, CHECKER_WHITE_COLOR, CELL_BLACK_COLOR, 12, 50)
        self.assertEqual(True, checker_1.is_in_borders(checker_1.x, checker_1.y))
        self.assertEqual(True, checker_2.is_in_borders(checker_2.x, checker_2.y))
        self.assertEqual(False, checker_3.is_in_borders(checker_3.x, checker_3.y))
        self.assertEqual(False, checker_4.is_in_borders(checker_4.x, checker_4.y))
        self.assertEqual(False, checker_5.is_in_borders(checker_5.x, checker_5.y))
        self.assertEqual(True, checker_6.is_in_borders(checker_6.x, checker_6.y))
        self.assertEqual(True, checker_7.is_in_borders(checker_7.x, checker_7.y))

    def test_set_game_mode(self):
        mode_1 = "mode"
        mode_2 = "123"
        mode_3 = None
        mode_4 = 42
        app = QApplication(sys.argv)
        start_window = StartMenu()
        start_window.set_game_mode(mode_1)
        self.assertEqual(mode_1, start_window.game_mode)
        start_window.set_game_mode(mode_2)
        self.assertEqual(mode_2, start_window.game_mode)
        start_window.set_game_mode(mode_3)
        self.assertEqual(mode_3, start_window.game_mode)
        start_window.set_game_mode(mode_4)
        self.assertEqual(mode_4, start_window.game_mode)
        app.quit()

    def test_set_dimension(self):
        dim_1 = None
        dim_2 = "123"
        dim_3 = "abc"
        dim_4 = "00020"
        dim_5 = "-10"
        dim_6 = "2.4"
        app = QApplication(sys.argv)
        start_window = StartMenu()
        with self.assertRaises(TypeError) as type_context:
            start_window.set_dimension(dim_1)
        self.assertTrue('This is error type!' in str(type_context.exception))
        start_window.set_dimension(dim_2)
        self.assertEqual(int(dim_2), start_window.field_dimension)
        with self.assertRaises(ValueError) as value_context:
            start_window.set_dimension(dim_3)
        self.assertTrue('This is error value!' in str(value_context.exception))
        start_window.set_dimension(dim_4)
        self.assertEqual(int(dim_4), start_window.field_dimension)
        start_window.set_dimension(dim_5)
        self.assertEqual(int(dim_5), start_window.field_dimension)
        with self.assertRaises(ValueError) as value_context:
            start_window.set_dimension(dim_6)
        self.assertTrue('This is error value!' in str(value_context.exception))
        app.quit()

    def test_set_start_player_color(self):
        app = QApplication(sys.argv)
        start_window = StartMenu()
        start_window.set_start_player_color('Black')
        self.assertEqual(CHECKER_BLACK_COLOR, start_window.really_player_color)
        start_window.set_start_player_color('White')
        self.assertEqual(CHECKER_WHITE_COLOR, start_window.really_player_color)
        with self.assertRaises(Exception) as context:
            start_window.set_start_player_color("Other")
        self.assertTrue('Error color!' in str(context.exception))
        app.quit()

    def test_get_value(self):
        app = QApplication(sys.argv)
        start_window = StartMenu()
        dict = {'word': 1, 'word2': 2, 'word3': 3}
        correct_value1 = start_window.get_value('word', dict)
        correct_value2 = start_window.get_value('word2', dict)
        correct_value3 = start_window.get_value('word3', dict)
        self.assertEqual(1, correct_value1)
        self.assertEqual(2, correct_value2)
        self.assertEqual(3, correct_value3)
        with self.assertRaises(ValueError) as context:
            start_window.get_value('w', dict)
        self.assertTrue('This is error value!' in str(context.exception))
        with self.assertRaises(TypeError) as context:
            start_window.get_value(None, dict)
        self.assertTrue('This is error type!' in str(context.exception))
        correct_value4 = start_window.get_value('5', dict)
        correct_value5 = start_window.get_value('67', dict)
        correct_value6 = start_window.get_value('100', dict)
        self.assertEqual(5, correct_value4)
        self.assertEqual(67, correct_value5)
        self.assertEqual(100, correct_value6)
        app.quit()

    def test_create_king_cells(self):
        field = Field(Player(CHECKER_WHITE_COLOR, set()), Player(CHECKER_BLACK_COLOR, set()), 10, 50)
        correct_white_cells = [(0, y) for y in range(field.field_dimension)]
        correct_black_cells = [(field.field_dimension - 1, y) for y in range(field.field_dimension)]
        self.assertEqual(correct_white_cells, field.king_checkers[CHECKER_WHITE_COLOR.getRgb()])
        self.assertEqual(correct_black_cells, field.king_checkers[CHECKER_BLACK_COLOR.getRgb()])
        field_2 = Field(Player(CHECKER_WHITE_COLOR, set()), Player(CHECKER_BLACK_COLOR, set()), 50, 50)
        correct_white_cells = [(0, y) for y in range(field_2.field_dimension)]
        correct_black_cells = [(field_2.field_dimension - 1, y) for y in range(field_2.field_dimension)]
        self.assertEqual(correct_white_cells, field_2.king_checkers[CHECKER_WHITE_COLOR.getRgb()])
        self.assertEqual(correct_black_cells, field_2.king_checkers[CHECKER_BLACK_COLOR.getRgb()])
        field_3 = Field(Player(CHECKER_WHITE_COLOR, set()), Player(CHECKER_BLACK_COLOR, set()), 100, 50)
        correct_white_cells = [(0, y) for y in range(field_3.field_dimension)]
        correct_black_cells = [(field_3.field_dimension - 1, y) for y in range(field_3.field_dimension)]
        self.assertEqual(correct_white_cells, field_3.king_checkers[CHECKER_WHITE_COLOR.getRgb()])
        self.assertEqual(correct_black_cells, field_3.king_checkers[CHECKER_BLACK_COLOR.getRgb()])

    def test_check_is_king(self):
        app = QApplication(sys.argv)
        start_window = StartMenu()
        start_window.field_dimension = 10
        start_window.game_mode = 'PvP'
        start_window.really_player_color = CHECKER_WHITE_COLOR
        start_window.main_window = Board(start_window.field_dimension, white_set=set(), black_set=set(),
                                         game_mode=start_window.game_mode,
                                         really_player_color=start_window.really_player_color)
        field = start_window.main_window.board_widget.game_field
        field.field[0][1].checker_color = CHECKER_WHITE_COLOR
        field.field[field.field_dimension - 1][0].checker_color = CHECKER_BLACK_COLOR
        field.field[0][1].check_is_king(field, True)
        field.field[field.field_dimension - 1][0].check_is_king(field, True)
        self.assertEqual(False, field.field[0][1].is_king)
        self.assertEqual(False, field.field[field.field_dimension - 1][0].is_king)
        field.field[0][1].check_is_king(field, False)
        field.field[field.field_dimension - 1][0].check_is_king(field, False)
        self.assertEqual(True, field.field[0][1].is_king)
        self.assertEqual(True, field.field[field.field_dimension - 1][0].is_king)
        app.quit()

    def test_find_walking_checkers(self):
        app = QApplication(sys.argv)
        start_window = StartMenu()
        start_window.field_dimension = 10
        start_window.game_mode = 'PvP'
        start_window.really_player_color = CHECKER_WHITE_COLOR
        start_window.main_window = Board(start_window.field_dimension, white_set=set(), black_set=set(),
                                         game_mode=start_window.game_mode,
                                         really_player_color=start_window.really_player_color)
        widget = start_window.main_window.board_widget
        widget.find_walking_checkers()
        walking_checkers = [(checker.x, checker.y) for checker in widget.walking_checkers]
        correct_cells = [(y, 6) for y in range(widget.field_dimension) if y % 2 != 0]
        self.assertEqual(len(correct_cells), len(walking_checkers))
        for pair in walking_checkers:
            self.assertTrue(pair in correct_cells)
        app.quit()

    def test_check_is_someone_winner(self):
        app = QApplication(sys.argv)
        start_window = StartMenu()
        start_window.field_dimension = 10
        start_window.game_mode = 'PvP'
        start_window.really_player_color = CHECKER_WHITE_COLOR
        start_window.main_window = Board(start_window.field_dimension, white_set=set(), black_set=set(),
                                         game_mode=start_window.game_mode,
                                         really_player_color=start_window.really_player_color)
        widget = start_window.main_window.board_widget
        widget.game_field.white_player.checkers_count = 0
        widget.check_is_someone_winner()
        self.assertEqual(True, widget.is_black_winner)
        widget.game_field.white_player.checkers_count = 1
        widget.game_field.black_player.checkers_count = 0
        widget.check_is_someone_winner()
        self.assertEqual(True, widget.is_white_winner)
        widget.game_field.white_player.checkers_count = 1
        widget.game_field.black_player.checkers_count = 1
        widget.is_white_winner = False
        widget.is_black_winner = False
        widget.check_is_someone_winner()
        self.assertEqual(False, widget.is_white_winner)
        self.assertEqual(False, widget.is_black_winner)
        app.quit()

    def test_change_player(self):
        app = QApplication(sys.argv)
        start_window = StartMenu()
        start_window.field_dimension = 10
        start_window.game_mode = 'PvP'
        start_window.really_player_color = CHECKER_WHITE_COLOR
        start_window.main_window = Board(start_window.field_dimension, white_set=set(), black_set=set(),
                                         game_mode=start_window.game_mode,
                                         really_player_color=start_window.really_player_color)
        widget = start_window.main_window.board_widget
        self.assertEqual(CHECKER_WHITE_COLOR, widget.current_player.color)
        widget.players = {widget.game_field.white_player: widget.game_field.black_player,
                          widget.game_field.black_player: widget.game_field.white_player}
        widget.change_player()
        self.assertTrue(widget.walking_checkers == [])
        self.assertEqual(CHECKER_BLACK_COLOR, widget.current_player.color)
        app.quit()

    def test_is_cut_possible(self):
        white_player = Player(CHECKER_WHITE_COLOR, set())
        black_player = Player(CHECKER_BLACK_COLOR, set())
        dict = {'True': True,
                'False': False,
                'None': None}
        field = Field(white_player, black_player, 10, 50)
        for_test_dir = path.join(SCRIPT_DIR, 'for_tests')
        with open(path.join(for_test_dir, 'field_1.txt'), 'r', encoding='utf-8') as f:
            lines = [line.split('#') for line in f.read().split('\n')]
        x = y = 0
        for line in lines:
            if line[3] == 'None':
                color = None
            else:
                line[3] = line[3].replace('(', '').replace(')', '').split(',')
                color = QColor(int(line[3][0]), int(line[3][1]), int(line[3][2]))
            line[4] = line[4].replace('(', '').replace(')', '').split(',')
            field.field[x][y] = Cell(int(line[0]),
                                     int(line[1]),
                                     dict[line[2]],
                                     color,
                                     QColor(int(line[4][0]),
                                            int(line[4][1]),
                                            int(line[4][2])),
                                     int(line[5]),
                                     int(line[6]),
                                     dict[line[7]],
                                     dict[line[8]])
            y += 1
            if y == field.field_dimension:
                y = 0
                x += 1
        self.assertEqual(True, field.field[0][1].is_correct_cut(field.field[3][4], field))
        self.assertEqual(False, field.field[0][1].is_correct_cut(field.field[2][3], field))
        self.assertEqual(False, field.field[0][1].is_correct_cut(field.field[8][7], field))
        self.assertEqual(False, field.field[6][7].is_correct_cut(field.field[6][7], field))
        self.assertEqual(True, field.field[0][1].is_correct_cut(field.field[5][6], field))

    def test_is_step_possible(self):
        white_player = Player(CHECKER_WHITE_COLOR, set())
        black_player = Player(CHECKER_BLACK_COLOR, set())
        current_player = white_player
        field = Field(white_player, black_player, 10, 50)
        self.assertEqual(False, field.field[0][3].is_step_possible(field.field[5][6], current_player, field))
        self.assertEqual(True, field.field[6][5].is_step_possible(field.field[5][6], current_player, field))
        self.assertEqual(False, field.field[9][1].is_step_possible(field.field[8][3], current_player, field))
        field.field[9][1].is_king = True
        self.assertEqual(False, field.field[9][1].is_step_possible(field.field[8][3], current_player, field))
        field.field[6][5].is_king = True
        self.assertEqual(True, field.field[6][5].is_step_possible(field.field[5][6], current_player, field))

    def test_find_positions_after_step(self):
        white_player = Player(CHECKER_WHITE_COLOR, set())
        black_player = Player(CHECKER_BLACK_COLOR, set())
        dict = {'True': True,
                'False': False,
                'None': None}
        field = Field(white_player, black_player, 10, 50)
        for_test_dir = path.join(SCRIPT_DIR, 'for_tests')
        with open(path.join(for_test_dir, 'field_1.txt'), 'r', encoding='utf-8') as f:
            lines = [line.split('#') for line in f.read().split('\n')]
        x = y = 0
        for line in lines:
            if line[3] == 'None':
                color = None
            else:
                line[3] = line[3].replace('(', '').replace(')', '').split(',')
                color = QColor(int(line[3][0]), int(line[3][1]), int(line[3][2]))
            line[4] = line[4].replace('(', '').replace(')', '').split(',')
            field.field[x][y] = Cell(int(line[0]),
                                     int(line[1]),
                                     dict[line[2]],
                                     color,
                                     QColor(int(line[4][0]),
                                            int(line[4][1]),
                                            int(line[4][2])),
                                     int(line[5]),
                                     int(line[6]),
                                     dict[line[7]],
                                     dict[line[8]])
            y += 1
            if y == field.field_dimension:
                y = 0
                x += 1
        positions = [(c.x, c.y) for c in field.field[0][1].find_positions_after_step(white_player, field)]
        correct_positions = [(0, 1), (2, 1)]
        self.assertEqual(correct_positions, positions)
        positions = [(c.x, c.y) for c in field.field[9][0].find_positions_after_step(white_player, field)]
        correct_positions = []
        self.assertEqual(correct_positions, positions)
        positions = [(c.x, c.y) for c in field.field[3][6].find_positions_after_step(black_player, field)]
        correct_positions = [(5, 4)]
        self.assertEqual(correct_positions, positions)

    def test_get_enemies(self):
        white_player = Player(CHECKER_WHITE_COLOR, set())
        black_player = Player(CHECKER_BLACK_COLOR, set())
        dict = {'True': True,
                'False': False,
                'None': None}
        field = Field(white_player, black_player, 10, 50)
        for_test_dir = path.join(SCRIPT_DIR, 'for_tests')
        with open(path.join(for_test_dir, 'field_1.txt'), 'r', encoding='utf-8') as f:
            lines = [line.split('#') for line in f.read().split('\n')]
        x = y = 0
        for line in lines:
            if line[3] == 'None':
                color = None
            else:
                line[3] = line[3].replace('(', '').replace(')', '').split(',')
                color = QColor(int(line[3][0]), int(line[3][1]), int(line[3][2]))
            line[4] = line[4].replace('(', '').replace(')', '').split(',')
            field.field[x][y] = Cell(int(line[0]),
                                     int(line[1]),
                                     dict[line[2]],
                                     color,
                                     QColor(int(line[4][0]),
                                            int(line[4][1]),
                                            int(line[4][2])),
                                     int(line[5]),
                                     int(line[6]),
                                     dict[line[7]],
                                     dict[line[8]])
            y += 1
            if y == field.field_dimension:
                y = 0
                x += 1
        enemies = [(checker.x, checker.y) for checker in field.field[0][1].get_enemies(field.field[4][5], field)]
        correct_enemies = [(3, 2)]
        self.assertEqual(correct_enemies, enemies)
        enemies = field.field[5][0].get_enemies(field.field[7][2], field)
        correct_enemies = ['No cell']
        self.assertEqual(correct_enemies, enemies)
        enemies = [(checker.x, checker.y) for checker in field.field[5][4].get_enemies(field.field[2][7], field)]
        correct_enemies = [(6, 3)]
        self.assertEqual(correct_enemies, enemies)

    def test_find_positions_after_cut(self):
        white_player = Player(CHECKER_WHITE_COLOR, set())
        black_player = Player(CHECKER_BLACK_COLOR, set())
        dict = {'True': True,
                'False': False,
                'None': None}
        field = Field(white_player, black_player, 10, 50)
        for_test_dir = path.join(SCRIPT_DIR, 'for_tests')
        with open(path.join(for_test_dir, 'field_1.txt'), 'r', encoding='utf-8') as f:
            lines = [line.split('#') for line in f.read().split('\n')]
        x = y = 0
        for line in lines:
            if line[3] == 'None':
                color = None
            else:
                line[3] = line[3].replace('(', '').replace(')', '').split(',')
                color = QColor(int(line[3][0]), int(line[3][1]), int(line[3][2]))
            line[4] = line[4].replace('(', '').replace(')', '').split(',')
            field.field[x][y] = Cell(int(line[0]),
                                     int(line[1]),
                                     dict[line[2]],
                                     color,
                                     QColor(int(line[4][0]),
                                            int(line[4][1]),
                                            int(line[4][2])),
                                     int(line[5]),
                                     int(line[6]),
                                     dict[line[7]],
                                     dict[line[8]])
            y += 1
            if y == field.field_dimension:
                y = 0
                x += 1
        positions = [(c.x, c.y) for c in field.field[0][1].find_positions_after_cut(None, field, white_player)]
        correct_position = [(4, 3), (5, 4), (6, 5), (7, 6)]
        self.assertEqual(correct_position, positions)
        field.field[5][4].is_king = True
        positions = [(c.x, c.y) for c in field.field[5][4].find_positions_after_cut(None, field, white_player)]
        correct_position = [(0, 1), (7, 2), (8, 1)]
        self.assertEqual(correct_position, positions)
        positions = [(c.x, c.y) for c in
                     field.field[5][4].find_positions_after_cut(field.field[4][3], field, white_player)]
        correct_position = [(7, 2), (8, 1)]
        self.assertEqual(correct_position, positions)

    def test_find_longest_cut(self):
        white_player = Player(CHECKER_WHITE_COLOR, set())
        black_player = Player(CHECKER_BLACK_COLOR, set())
        dict = {'True': True,
                'False': False,
                'None': None}
        field = Field(white_player, black_player, 10, 50)
        for_test_dir = path.join(SCRIPT_DIR, 'for_tests')
        with open(path.join(for_test_dir, 'field_2.txt'), 'r', encoding='utf-8') as f:
            lines = [line.split('#') for line in f.read().split('\n')]
        x = y = 0
        for line in lines:
            if line[3] == 'None':
                color = None
            else:
                line[3] = line[3].replace('(', '').replace(')', '').split(',')
                color = QColor(int(line[3][0]), int(line[3][1]), int(line[3][2]))
            line[4] = line[4].replace('(', '').replace(')', '').split(',')
            field.field[x][y] = Cell(int(line[0]),
                                     int(line[1]),
                                     dict[line[2]],
                                     color,
                                     QColor(int(line[4][0]),
                                            int(line[4][1]),
                                            int(line[4][2])),
                                     int(line[5]),
                                     int(line[6]),
                                     dict[line[7]],
                                     dict[line[8]])
            y += 1
            if y == field.field_dimension:
                y = 0
                x += 1
        result_position = []
        field.field[3][0].find_longest_cut(None, field, result_position, white_player, field.field[3][0])
        result_position = []
        field.field[0][1].find_longest_cut(None, field, result_position, white_player, field.field[0][1])
        field.field[7][4].find_longest_cut(None, field, result_position, white_player, field.field[7][4])
        positions_1 = [(c.x, c.y) for c in field.field[3][0].positions[0]]
        positions_2 = [(c.x, c.y) for c in field.field[0][1].positions[0]]
        positions_3 = [(c.x, c.y) for c in field.field[7][4].positions[0]]
        correct_1 = [(2, 1), (4, 3), (6, 1), (8, 3), (6, 5)]
        correct_2 = [(6, 5), (8, 3), (6, 1), (4, 3), (2, 5)]
        correct_3 = []
        self.assertTrue(len(positions_1) == len(positions_2))
        self.assertEqual(correct_1, positions_1)
        self.assertEqual(correct_2, positions_2)
        self.assertEqual(correct_3, positions_3)
        field.field[0][1].positions = []
        field.field[0][1].find_longest_cut(field.field[3][4], field, result_position, white_player, field.field[0][1])
        self.assertEqual([[]], field.field[0][1].positions)

    def test_move(self):
        white_player = Player(CHECKER_WHITE_COLOR, set())
        black_player = Player(CHECKER_BLACK_COLOR, set())
        dict = {'False': False, 'None': None, 'True': True, }
        field = Field(white_player, black_player, 10, 50)
        for_test_dir = path.join(SCRIPT_DIR, 'for_tests')
        with open(path.join(for_test_dir, 'field_2.txt'), 'r', encoding='utf-8') as f:
            lines = [line.split('#') for line in f.read().split('\n')]
        x = y = 0
        for line in lines:
            if line[3] == 'None':
                color = None
            else:
                line[3] = line[3].replace('(', '').replace(')', '').split(',')
                color = QColor(int(line[3][0]), int(line[3][1]), int(line[3][2]))
            line[4] = line[4].replace('(', '').replace(')', '').split(',')
            field.field[x][y] = Cell(int(line[0]),
                                     int(line[1]),
                                     dict[line[2]],
                                     color,
                                     QColor(int(line[4][0]),
                                            int(line[4][1]),
                                            int(line[4][2])),
                                     int(line[5]),
                                     int(line[6]),
                                     dict[line[7]],
                                     dict[line[8]])
            y += 1
            if y == field.field_dimension:
                y = 0
                x += 1
        walking_checkers = []
        test_checker = field.field[6][3]
        test_checker.positions.append(field.field[5][2])
        white_player.add_checker(test_checker)
        walking_checkers.append(test_checker)
        test_checker.move(field.field[5][2], white_player, walking_checkers)
        self.assertTrue(test_checker not in walking_checkers)
        self.assertTrue(not test_checker.is_king)
        self.assertTrue(test_checker.checker_color is None)
        self.assertTrue(test_checker.positions == [])

    def test_load_game(self):
        raised = False
        try:
            app = QApplication(sys.argv)
            start_window = StartMenu()
            start_window.load_game(run_in_test=True)
            app.quit()
        except:
            raised = True
        self.assertTrue(not raised)

    def test_start_game(self):
        raised = False
        try:
            app = QApplication(sys.argv)
            start_window = StartMenu()
            start_window.start_game(run_in_test=True)
            app.quit()
        except:
            raised = True
        self.assertTrue(not raised)


if __name__ == '__main__':
    unittest.main()
