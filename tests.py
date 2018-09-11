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


if __name__ == '__main__':
    unittest.main()
