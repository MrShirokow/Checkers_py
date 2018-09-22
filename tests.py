import unittest
from player import *
from cell import *
from field import *
from PyQt5.QtGui import QPainter
from startMenu import *


class StartTests(unittest.TestCase):
    def test_add_and_remove_checker(self):
        player = Player(CHECKER_WHITE_COLOR, True, set())
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
        field_1 = Field(Player(CHECKER_WHITE_COLOR, True, set()), Player(CHECKER_BLACK_COLOR, True, set()), 10, 50)
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
        field = Field(Player(CHECKER_WHITE_COLOR, False, set()), Player(CHECKER_BLACK_COLOR, True, set()), 10, 50)
        correct_white_cells = [(0, y) for y in range(field.field_dimension)]
        correct_black_cells = [(field.field_dimension - 1, y) for y in range(field.field_dimension)]
        self.assertEqual(correct_white_cells, field.king_checkers[CHECKER_WHITE_COLOR.getRgb()])
        self.assertEqual(correct_black_cells, field.king_checkers[CHECKER_BLACK_COLOR.getRgb()])
        field_2 = Field(Player(CHECKER_WHITE_COLOR, False, set()), Player(CHECKER_BLACK_COLOR, True, set()), 50, 50)
        correct_white_cells = [(0, y) for y in range(field_2.field_dimension)]
        correct_black_cells = [(field_2.field_dimension - 1, y) for y in range(field_2.field_dimension)]
        self.assertEqual(correct_white_cells, field_2.king_checkers[CHECKER_WHITE_COLOR.getRgb()])
        self.assertEqual(correct_black_cells, field_2.king_checkers[CHECKER_BLACK_COLOR.getRgb()])
        field_3 = Field(Player(CHECKER_WHITE_COLOR, False, set()), Player(CHECKER_BLACK_COLOR, True, set()), 100, 50)
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


if __name__ == '__main__':
    unittest.main()
