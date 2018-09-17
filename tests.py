import unittest
from player import *
from cell import *
from field import *
from PyQt5.QtGui import QPainter


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


if __name__ == '__main__':
    unittest.main()
